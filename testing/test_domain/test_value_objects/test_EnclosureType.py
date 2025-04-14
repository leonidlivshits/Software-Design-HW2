import pytest

from domain.value_objects.EnclosureType import EnclosureType


def test_enclosure_type_validation():
    with pytest.raises(ValueError, match="Недопустимый тип вольера"):
        EnclosureType("invalid_type")

def test_enclosure_type_equality():
    et1 = EnclosureType("predator")
    et2 = EnclosureType("predator")
    assert et1 == et2
