from domain.entities.FeedingShedule import FeedingSchedule
from domain.events.FeedingTimeEvent import FeedingTimeEvent
from domain.repositories.IAnimalRepository import IAnimalRepository
from domain.repositories.IFeedingScheduleRepository import IFeedingScheduleRepository


class FeedingOrganizationService:
    def __init__(
        self,
        animal_repo: IAnimalRepository,
        feeding_repo: IFeedingScheduleRepository
    ):
        self.animal_repo = animal_repo
        self.feeding_repo = feeding_repo

    def feed_animal(self, animal_id: str, food_type: str) -> None:
        animal = self.animal_repo.get_by_id(animal_id)
        if not animal:
            raise ValueError("Животное не найдено")
        if not animal.is_healthy:
            raise ValueError("Животное больно! Вылечите его, чтобы кормить!")
        if food_type != animal.species.food_type:
            raise ValueError("Неверный тип пищи для этого вида")

        animal.feed(food_type)
        self.animal_repo.save(animal)

    def add_feeding_schedule(self, schedule: FeedingSchedule) -> FeedingTimeEvent:
        self.feeding_repo.save(schedule)
        return FeedingTimeEvent(
            schedule_id=schedule.id,
            animal_id=schedule.animal.id,
            feeding_time=schedule.feeding_time.value.strftime("%H:%M")
        )