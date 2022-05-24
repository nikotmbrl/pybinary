import abc


class ISerializable(abc.ABC, type):
    @abc.abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: bytes) -> object:
        raise NotImplementedError()
