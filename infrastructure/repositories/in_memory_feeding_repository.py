from collections import defaultdict

from domain.entities.FeedingShedule import FeedingSchedule
from domain.repositories.IFeedingScheduleRepository import IFeedingScheduleRepository


class InMemoryFeedingScheduleRepository(IFeedingScheduleRepository):
    def __init__(self):
        self.schedules = {}  # {schedule_id: FeedingSchedule}
        #self.counter = 0
        self.animal_schedules = defaultdict(list)  # {animal_id: list[FeedingSchedule]}

    def save(self, schedule: FeedingSchedule) -> None:
        #self.counter += 1
        # self.schedules[schedule.id] = schedule
        # self.animal_schedules[schedule.animal.id].append(schedule)

        self.schedules[schedule.id] = schedule
        animal_id = schedule.animal.id
        self.animal_schedules[animal_id] = [
            s for s in self.animal_schedules[animal_id] if s.id != schedule.id
        ]
        self.animal_schedules[animal_id].append(schedule)


    def get_by_animal_id(self, animal_id: str) -> list[FeedingSchedule]:
        return self.animal_schedules.get(animal_id, [])
    
    def get_all(self):
        return list(self.schedules.values())
    
    def get_by_id(self, schedule_id: str):
        return self.schedules.get(schedule_id)