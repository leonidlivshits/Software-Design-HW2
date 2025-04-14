import pytest
from domain.entities.Animal import Animal
from domain.value_objects.Species import Species


def test_animal_feeding_healthy_correct_food():
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male", is_healthy=True)
    animal.feed("meat")

def test_animal_feeding_healthy_wrong_food():
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male", is_healthy=True)
    with pytest.raises(ValueError, match="отказывается есть эту пищу"):
        animal.feed("grass")

def test_animal_feeding_sick_animal():
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male", is_healthy=False)
    with pytest.raises(ValueError, match="Невозможно кормить больное животное"):
        animal.feed("meat")

def test_animal_heal():
    animal = Animal("1", Species("lion"), "Simba", "2000-01-01", "male", is_healthy=False)
    animal.heal()
    assert animal.is_healthy is True