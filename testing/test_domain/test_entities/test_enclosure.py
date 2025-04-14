import pytest
from domain.entities.Animal import Animal
from domain.entities.Enclosure import Enclosure
from domain.value_objects.EnclosureType import EnclosureType
from domain.value_objects.Species import Species


def test_add_animal_to_enclosure():
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male")
    enclosure = Enclosure("e1", EnclosureType("predator"), 2)
    
    enclosure.add_animal(animal)
    assert len(enclosure.current_animals) == 1
    assert animal.enclosure_id == "e1"

def test_enclosure_capacity_limit():
    species = Species("lion")
    animal1 = Animal("1", species, "Simba", "2000-01-01", "male")
    animal2 = Animal("2", species, "Mufasa", "1990-01-01", "male")
    enclosure = Enclosure("e1", EnclosureType("predator"), 1)
    
    enclosure.add_animal(animal1)
    with pytest.raises(ValueError):
        enclosure.add_animal(animal2)