# infrastructure/repositories/in_memory_feeding_repository.py
from collections import defaultdict

from domain.entities.FeedingShedule import FeedingSchedule
from domain.repositories.IFeedingScheduleRepository import IFeedingScheduleRepository


class InMemoryFeedingScheduleRepository(IFeedingScheduleRepository):
    def __init__(self):
        self.schedules = {}  # {schedule_id: FeedingSchedule}
        self.animal_schedules = defaultdict(list)  # {animal_id: list[FeedingSchedule]}

    def save(self, schedule: FeedingSchedule) -> None:
        self.schedules[schedule.id] = schedule
        self.animal_schedules[schedule.animal.id].append(schedule)

    def get_by_animal_id(self, animal_id: str) -> list[FeedingSchedule]:
        return self.animal_schedules.get(animal_id, [])