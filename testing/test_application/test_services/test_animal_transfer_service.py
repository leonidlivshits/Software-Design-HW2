import pytest

from domain.entities.Animal import Animal
from domain.entities.Enclosure import Enclosure
from domain.events.AnimalMovedEvent import AnimalMovedEvent
from domain.value_objects.EnclosureType import EnclosureType
from domain.value_objects.Species import Species

def test_successful_animal_transfer(transfer_service, animal_repo, enclosure_repo):
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male", is_healthy=True)
    enclosure = Enclosure("e1", EnclosureType("predator"), 5)
    
    animal_repo.save(animal)
    enclosure_repo.save(enclosure)

    event = transfer_service.move_animal("1", "e1")

    assert animal.enclosure_id == "e1"
    assert len(enclosure.current_animals) == 1
    assert isinstance(event, AnimalMovedEvent)

def test_transfer_to_incompatible_enclosure(transfer_service, animal_repo, enclosure_repo):
    species = Species("bat")
    animal = Animal("1", species, "Batman", "2000-01-01", "male", is_healthy=True)
    enclosure = Enclosure("e1", EnclosureType("predator"), 5)
    
    animal_repo.save(animal)
    enclosure_repo.save(enclosure)
    
    with pytest.raises(ValueError, match="не совместим с видом"):
        transfer_service.move_animal("1", "e1")

def test_transfer_to_full_enclosure(transfer_service, animal_repo, enclosure_repo):
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male", is_healthy=True)
    enclosure = Enclosure("e1", EnclosureType("predator"), 1)
    
    enclosure.add_animal(Animal("2", species, "Nala", "2000-01-01", "female"))
    enclosure_repo.save(enclosure)
    animal_repo.save(animal)
    
    with pytest.raises(ValueError, match="переполнен"):
        transfer_service.move_animal("1", "e1")