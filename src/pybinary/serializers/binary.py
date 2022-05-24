from pybinary._impl.binary import SimpleTypesMapping, Field, StructureDescription, StringFactory, ArrayFactory


# class Endianness:
#     def __init__(self, base_type: SimpleTypesMapping):
#         self._field_type = base_type


class BinarySerializable(metaclass=StructureDescription):
    def __getattribute__(self, key):
        value = super().__getattribute__(key)
        if isinstance(value, Field):
            return value.get()
        return value

    def __setattr__(self, key, value):
        if hasattr(self, key):
            current = super().__getattribute__(key)
            if isinstance(current, Field):
                if not isinstance(value, Field):
                    return current.set(value)
            super().__setattr__(key, value)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")

    def serialize(self) -> bytes:
        pass

    @classmethod
    def deserialize(cls, data: bytes) -> object:
        pass


class FieldTypes:
    Int8 = SimpleTypesMapping.Int8
    Int16 = SimpleTypesMapping.Int16
    Int32 = SimpleTypesMapping.Int32
    Int64 = SimpleTypesMapping.Int64
    UInt8 = SimpleTypesMapping.UInt8
    UInt16 = SimpleTypesMapping.UInt16
    UInt32 = SimpleTypesMapping.UInt32
    UInt64 = SimpleTypesMapping.UInt64
    Float = SimpleTypesMapping.Float
    Double = SimpleTypesMapping.Double
    String = StringFactory
    Array = ArrayFactory
