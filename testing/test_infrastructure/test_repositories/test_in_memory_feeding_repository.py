
from datetime import time
from domain.entities.Animal import Animal
from domain.entities.FeedingShedule import FeedingSchedule

from domain.value_objects.FeedingTime import FeedingTime
from domain.value_objects.Species import Species


def test_feeding_schedule_repository_save(feeding_repo):
    animal = Animal("1", Species("lion"), "Simba", "2020-01-01", "male")
    schedule = FeedingSchedule("1", animal, FeedingTime(12, 15), "meat")
    
    feeding_repo.save(schedule)
    assert feeding_repo.get_by_id("1") == schedule
    assert schedule in feeding_repo.get_by_animal_id("1")
    assert feeding_repo.get_all() == [schedule]