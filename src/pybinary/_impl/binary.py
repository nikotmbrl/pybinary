import codecs
import enum
import struct
import typing
from abc import ABC

from pybinary._utils.utils import get_caller_signature
from pybinary.abstract.iserializable import ISerializable


class SimpleTypesMapping(enum.Enum):
    Int8 = "{size}b"
    Int16 = "{size}h"
    Int32 = "{size}i"
    Int64 = "{size}q"
    UInt8 = "{size}B"
    UInt16 = "{size}H"
    UInt32 = "{size}I"
    UInt64 = "{size}Q"
    Float = "{size}f"
    Double = "{size}d"


class FieldReference:
    def __init__(self, obj: object, field_name: str | None = None):
        self._field_name = field_name
        self._obj = obj

    def get(self):
        if self._field_name:
            return getattr(self._obj, self._field_name)
        elif isinstance(self._obj, Field):
            return self._obj
        raise ValueError()


class Field:
    def __init__(self, field_type: SimpleTypesMapping, _size: int | FieldReference | None = None, codec: codecs.CodecInfo | None = None):
        self._type = field_type
        self._format = field_type.value
        self._is_fixed_size = True
        self._element_size = 1
        self._codec = codec
        if self._codec is not None:
            _data, _number_of_elements = codec.encode("test string")
            self._element_size = len(_data) // _number_of_elements
            assert (len(_data) % _number_of_elements) == 0
        self._is_collection = _size is not None
        self._number_of_elements = 1 if _size is None else _size
        if isinstance(_size, FieldReference):
            self._is_fixed_size = False
            self._data = b""
            self._size = None
            self._number_of_elements = _size
        else:
            self._size = struct.calcsize(str.format(self._format, size=self._number_of_elements * self._element_size))
            self._data = b"\x00" * self._size

    def format(self):
        if isinstance(self._number_of_elements, FieldReference):
            referenced_size = self._number_of_elements.get()
            return str.format(self._format, size=referenced_size.get()  * self._element_size)
        return str.format(self._format, size=self._number_of_elements * self._element_size)

    def get(self) -> typing.Any:
        value = struct.unpack(self.format(), self._data)
        if not self._is_collection:
            value = value[0]
        if self._codec:
            return self._codec.decode(bytes(value))[0]
        return value

    def set(self, value: typing.Any):
        if self._codec:
            value = self._codec.encode(value)[0]
        if isinstance(value, typing.Collection):
            data = struct.pack(self.format(), *value)
        else:
            data = struct.pack(self.format(), value)

        self._data = data


class StructureDescription(ISerializable, ABC):
    def __new__(cls, name: str, bases: tuple, namespace: dict, **kwargs):
        for value in namespace:
            if value.startswith("__"):
                continue
            for base in bases:
                if hasattr(base, value):
                    raise ValueError(f"Overriding inherited field '{value}' of class '{base.__name__}' in class '{name}'")
        new_obj = super().__new__(cls, name, bases, namespace)
        for field_name, field_value in namespace.items():
            if isinstance(field_value, SimpleTypesMapping):
                setattr(new_obj, field_name, Field(field_value))
            elif isinstance(field_value, BasicContainerFactory):
                setattr(new_obj, field_name, field_value.create(new_obj))

        return new_obj


class BasicContainerFactory:
    def __init__(self, size: int | SimpleTypesMapping):
        if isinstance(size, SimpleTypesMapping):
            signature = get_caller_signature(self.__init__)
            size = signature.arguments["size"]
        self._size = size

    def create(self, object_ref: object):
        raise NotImplementedError()

    def _create(self, object_ref: object):
        size = self._size
        if isinstance(self._size, str):
            size = FieldReference(field_name=self._size, obj=object_ref)
        if isinstance(self._size, Field):
            size = FieldReference(obj=self._size)
        return size


class StringFactory(BasicContainerFactory):
    def __init__(self, size: int | SimpleTypesMapping, encoding: str = "utf-8"):
        super().__init__(size)
        self._codec = codecs.lookup(encoding)

    def create(self, object_ref: object) -> Field:
        size = super()._create(object_ref)
        return Field(
            field_type=SimpleTypesMapping.UInt8,
            _size=size,
            codec=self._codec
        )


class ArrayFactory(BasicContainerFactory):
    def __init__(self, size: int | SimpleTypesMapping, element_type: SimpleTypesMapping = SimpleTypesMapping.UInt8):
        super().__init__(size)
        self._element_type = element_type

    def create(self, object_ref: object) -> Field:
        size = super()._create(object_ref)
        return Field(
            field_type=self._element_type,
            _size=size,
        )