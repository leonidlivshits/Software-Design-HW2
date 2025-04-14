
from domain.entities.Animal import Animal
from domain.entities.Enclosure import Enclosure
from domain.value_objects.EnclosureType import EnclosureType
from domain.value_objects.Species import Species


def test_free_enclosures(stats_service, enclosure_repo):
    enclosure1 = Enclosure("e1", EnclosureType("predator"), 2)
    enclosure2 = Enclosure("e2", EnclosureType("herbivore"), 1)
    enclosure_repo.save(enclosure1)
    enclosure_repo.save(enclosure2)
    
    free = stats_service.get_free_enclosures()
    assert len(free) == 2

def test_get_animal_count_empty(stats_service):
    assert stats_service.get_animal_count() == 0

def test_get_animal_count_after_adding(stats_service, animal_repo):
    animal = Animal("1", Species("lion"), "Simba", "2000-01-01", "male")
    animal_repo.save(animal)
    assert stats_service.get_animal_count() == 1

