import random
import string
import struct
import typing
import uuid

from pybinary.serializers.binary import FieldTypes, BinarySerializable


class Helpers:
    @staticmethod
    def generate_value(value_type: FieldTypes, number_of_elements: None | int = None):
        match value_type:
            case FieldTypes.Int8:
                generator = random.randint
                minmax = (-0x80, 0x7F)
            case FieldTypes.Int16:
                generator = random.randint
                minmax = (-0x8000, 0x7FFF)
            case FieldTypes.Int32:
                generator = random.randint
                minmax = (-0x80000000, 0x7FFFFFFF)
            case FieldTypes.Int64:
                generator = random.randint
                minmax = (-0x8000000000000000, 0x7FFFFFFFFFFFFFFF)
            case FieldTypes.UInt8:
                generator = random.randint
                minmax = (0x0, 0xFF)
            case FieldTypes.UInt16:
                generator = random.randint
                minmax = (0x0, 0xFFFF)
            case FieldTypes.UInt32:
                generator = random.randint
                minmax = (0x0, 0xFFFFFFFF)
            case FieldTypes.UInt64:
                generator = random.randint
                minmax = (0x0, 0xFFFFFFFFFFFFFFFF)
            case FieldTypes.Float:
                generator = lambda: struct.unpack("f", struct.pack("f", random.random()))[0]
                minmax = ()
            case FieldTypes.Double:
                generator = random.random
                minmax = ()
            case FieldTypes.String:
                generator = random.choice
                minmax = (string.printable,)
                if number_of_elements is None or number_of_elements < 1:
                    number_of_elements = random.randint(1, 255)

        if number_of_elements is None:
            return generator(*minmax)
        else:
            result = tuple(generator(*minmax) for _ in range(number_of_elements))
            if value_type == FieldTypes.String:
                return "".join(result)
            return result

    @staticmethod
    def create_sample_class(fields: typing.Dict[str, FieldTypes]) -> typing.ClassVar:
        dynamic_class_instance = type(f"class_{uuid.uuid4().hex}", (BinarySerializable,), fields)
        return dynamic_class_instance