import json
import zlib
import enum

class SerializationType(enum.Enum):
    STRING = 0
    BYTES = 1
    COMPRESSED_BYTES = 2

class Serializer:
    def __init__(self, compression_level: int = 4):
        self.compression_level = compression_level


    def serialize(self, data: object, serialization_type = SerializationType.STRING) -> str | bytes:
        disected_data = self.disect(data)
        disected_data_json = json.dumps(disected_data)

        if serialization_type == SerializationType.BYTES: return disected_data_json.encode('utf-8')
        if serialization_type == SerializationType.COMPRESSED_BYTES:
            return zlib.compress(
                disected_data_json.encode('utf-8'),
                self.compression_level
            )
        if serialization_type == SerializationType.STRING: return disected_data_json


    def disect(self, obj: object) -> list:
        result = []
        for attr in dir(obj):
            if attr == 'pyobj_serialization_name': continue
            value = getattr(obj, attr)
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, list) or isinstance(value, dict) or isinstance(value, bool) or isinstance(value, float):
                result.append((attr, value))


        return result


serializer = Serializer()
print(serializer.serialize([1, 2, 3]))
