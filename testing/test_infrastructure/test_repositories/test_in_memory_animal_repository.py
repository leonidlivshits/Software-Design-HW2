from domain.entities.Animal import Animal
from domain.value_objects.Species import Species


def test_animal_repository_save_and_get(animal_repo):
    animal = Animal("1", Species("lion"), "Simba", "2020-01-01", "male")
    animal_repo.save(animal)
    assert animal_repo.get_by_id("1") == animal
    assert animal_repo.get_animal_count() == 1
    animal_repo.delete("1")
    assert animal_repo.get_animal_count() == 0
