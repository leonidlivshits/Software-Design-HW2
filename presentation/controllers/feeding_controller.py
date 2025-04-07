# presentation/controllers/feeding_controller.py
from fastapi import APIRouter, Depends, HTTPException, status

from domain.entities.FeedingShedule import FeedingSchedule
from domain.value_objects.FeedingTime import FeedingTime
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from infrastructure.repositories.in_memory_feeding_repository import InMemoryFeedingScheduleRepository
from application.services.feeding_organization_service import FeedingOrganizationService
from presentation.container import get_feeding_repo, get_feeding_service, get_animal_repo
from datetime import time

router = APIRouter(prefix="/feeding-schedules")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_feeding_schedule(
    animal_id: str,
    feeding_time_hour: int,
    feeding_time_minute: int,
    food_type: str,
    feeding_repo: InMemoryFeedingScheduleRepository = Depends(get_feeding_repo),
    animal_repo: InMemoryAnimalRepository = Depends(get_animal_repo),
    feeding_service: FeedingOrganizationService = Depends(get_feeding_service)
):
    try:
        # Проверка существования животного
        animal = animal_repo.get_by_id(animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found")

        # Валидация времени кормления
        feeding_time = FeedingTime(feeding_time_hour, feeding_time_minute)

        # Создание расписания
        schedule = FeedingSchedule(
            id=str(len(feeding_repo.get_all()) + 1),
            animal=animal,
            feeding_time=feeding_time,
            food_type=food_type
        )

        # Сохранение через сервис (генерация события)
        event = feeding_service.add_feeding_schedule(schedule)
        return {"id": schedule.id, "event": event.__dict__}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all_schedules(feeding_repo: InMemoryFeedingScheduleRepository = Depends(get_feeding_repo)):
    return feeding_repo.get_all()

@router.get("/{schedule_id}")
def get_schedule(
    schedule_id: str,
    feeding_repo: InMemoryFeedingScheduleRepository = Depends(get_feeding_repo)
):
    schedule = feeding_repo.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.post("/{schedule_id}/complete")
def mark_as_completed(
    schedule_id: str,
    feeding_repo: InMemoryFeedingScheduleRepository = Depends(get_feeding_repo)
):
    schedule = feeding_repo.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.mark_as_completed()
    feeding_repo.save(schedule)
    return {"message": "Schedule marked as completed"}