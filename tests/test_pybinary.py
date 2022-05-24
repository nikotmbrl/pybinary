import random

from pybinary.serializers.binary import FieldTypes

import pytest

from tests.helpers import Helpers


class TestBinarySerializable:
    @pytest.mark.parametrize(
        "test_type", [
            FieldTypes.Int8,
            FieldTypes.Int16,
            FieldTypes.Int32,
            FieldTypes.Int64,
            FieldTypes.Int8,
            FieldTypes.Int16,
            FieldTypes.Int32,
            FieldTypes.Int64,
            FieldTypes.Float,
            FieldTypes.Double
        ]
    )
    @pytest.mark.parametrize("size", [None, 1, 255, random.randint(2, 254)])
    def test_simple_types_assignment(self, test_type, size):
        value = Helpers.generate_value(test_type, size)
        if size is None:
            cls = Helpers.create_sample_class({"field_1": test_type})
        else:
            cls = Helpers.create_sample_class({"field_1": FieldTypes.Array(size, element_type=test_type)})
        obj = cls()
        obj.field_1 = value
        assert obj.field_1 == value

    @pytest.mark.parametrize("size", [1, 255, random.randint(2, 254)])
    @pytest.mark.parametrize("encoding", ["utf-8", "ascii", "utf-16le"])
    def test_strings_assignment(self, size, encoding):
        value = Helpers.generate_value(FieldTypes.String, size)
        cls = Helpers.create_sample_class({"field_1": FieldTypes.String(size, encoding=encoding)})
        obj = cls()
        obj.field_1 = value
        assert obj.field_1 == value
