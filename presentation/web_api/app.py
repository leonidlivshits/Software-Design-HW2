from fastapi import FastAPI

from application.services.animal_transfer_service import AnimalTransferService
from application.services.feeding_organization_service import FeedingOrganizationService
from application.services.zoo_statistics_service import ZooStatisticsService
from domain.events.AnimalMovedEvent import AnimalMovedEvent
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from infrastructure.repositories.in_memory_enclosure_repository import InMemoryEnclosureRepository
from infrastructure.repositories.in_memory_feeding_repository import InMemoryFeedingScheduleRepository
from presentation.container import container, get_animal_repo, get_enclosure_repo, get_feeding_repo, get_feeding_service, get_stats_service, get_transfer_service
from presentation.controllers import (
    animal_controller,
    enclosure_controller,
    feeding_controller,
    stats_controller
)
from infrastructure.event_bus import EventBus

app = FastAPI()

app.include_router(animal_controller.router)
app.include_router(enclosure_controller.router)
app.include_router(feeding_controller.router)
app.include_router(stats_controller.router)



app.dependency_overrides.update({
    InMemoryAnimalRepository: get_animal_repo,
    InMemoryEnclosureRepository: get_enclosure_repo,
    InMemoryFeedingScheduleRepository: get_feeding_repo,
    AnimalTransferService: get_transfer_service,
    FeedingOrganizationService: get_feeding_service,
    ZooStatisticsService: get_stats_service,
})

# Шина событий
event_bus = EventBus()

def log_animal_move(event):
    print(f"Animal {event.animal_id} moved from {event.old_enclosure_id} to {event.new_enclosure_id}")

event_bus.subscribe(AnimalMovedEvent, log_animal_move)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
