from datetime import time
from domain.entities.Animal import Animal
from domain.entities.FeedingShedule import FeedingSchedule
from domain.value_objects.FeedingTime import FeedingTime
from domain.value_objects.FeedingTime import FeedingTime
from domain.value_objects.Species import Species
import pytest

def test_mark_feeding_completed():
    animal = Animal("1", Species("lion"), "Simba", "2020-01-01", "male")
    schedule = FeedingSchedule("1", animal, FeedingTime(12, 15), "meat")
    
    schedule.mark_as_completed()
    assert schedule.is_completed