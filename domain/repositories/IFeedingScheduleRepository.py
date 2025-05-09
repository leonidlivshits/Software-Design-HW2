from domain.entities.FeedingShedule import FeedingSchedule


class IFeedingScheduleRepository:
    def save(self, schedule: FeedingSchedule) -> None: ...
    def get_by_animal_id(self, animal_id: str) -> FeedingSchedule: ...