import struct
import json


class trail_position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class trail:
    def __init__(self):
        self.file_name = None
        self.buffer = None
        self.version = None
        self.map_id = None
        self.positions = []

    def import_trl(self, file_name):
        self.file_name = file_name
        offset = 0

        with open(self.file_name, 'rb') as buffer:
            self.buffer = buffer.read()

        self.version, = struct.unpack_from(
            'i', self.buffer, offset)  # -> allways 0!
        offset += 4

        self.map_id, = struct.unpack_from('i', self.buffer, offset)
        offset += 4

        while offset < len(self.buffer):
            position_x, = struct.unpack_from('f', self.buffer, offset)
            position_y, = struct.unpack_from('f', self.buffer, offset + 4)
            position_z, = struct.unpack_from('f', self.buffer, offset + 8)

            self.positions.append(trail_position(
                position_x, position_y, position_z))
            offset += 12

    def class_to_b_string(self):
        trail_bytes = b""
        trail_bytes += struct.pack('i', self.version)
        trail_bytes += struct.pack('i', self.map_id)

        for pos in self.positions:
            trail_bytes += struct.pack('f', pos.x)
            trail_bytes += struct.pack('f', pos.y)
            trail_bytes += struct.pack('f', pos.z)

        return trail_bytes

    def export(self, file_name):
        trail_bytes = self.class_to_b_string()

        with open(file_name, 'wb') as buffer:
            buffer.write(trail_bytes)

    def to_json(self):
        result_json = {
            "version": self.version,
            "map_id": self.map_id,
            "positions": [
                {"x": p.x, "y": p.y, "z": p.z} for p in self.positions
            ]
        }

        return result_json

    def export_json(self, file_name):
        self.file_name = file_name

        with open(file_name, 'w') as open_file:
            json.dump(self.to_json(), open_file)

    def from_json(self, json_data):
        result_json = {
            "version": self.version,
            "map_id": self.map_id,
            "positions": [
                {"x": p.x, "y": p.y, "z": p.z} for p in self.positions
            ]
        }

        self.version = json_data.get("version")
        self.map_id = json_data.get("map_id")
        self.positions = [trail_position(p.get("x"), p.get(
            "y"), p.get("z")) for p in json_data.get("positions")]

        self.buffer = self.class_to_b_string()

        return result_json

    def import_json(self, file_name):
        self.file_name = file_name

        with open(file_name, 'r') as open_file:
            self.from_json(json.load(open_file))
