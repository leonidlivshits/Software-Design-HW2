# testing/test_application/test_services/test_feeding_organization_service.py
import pytest

from domain.entities.Animal import Animal
from domain.value_objects.Species import Species


def test_successful_feeding(feeding_service, animal_repo):
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male", is_healthy=True)
    animal_repo.save(animal)
    
    feeding_service.feed_animal("1", "meat")

    assert True

def test_feeding_with_wrong_food_type(feeding_service, animal_repo):
    species = Species("lion")
    animal = Animal("1", species, "Simba", "2000-01-01", "male")
    animal_repo.save(animal)
    
    with pytest.raises(ValueError):
        feeding_service.feed_animal("1", "grass")