# from fastapi import FastAPI

# from application.services.animal_transfer_service import AnimalTransferService
# from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
# from presentation.container import Container
# from presentation.controllers import (
#     animal_controller,
#     enclosure_controller,
#     feeding_controller,
#     stats_controller
# )
# from infrastructure.event_bus import EventBus

# app = FastAPI()
# container = Container()

# # Регистрация контроллеров
# app.include_router(animal_controller.router)
# app.include_router(enclosure_controller.router)
# app.include_router(feeding_controller.router)
# app.include_router(stats_controller.router)

# # # Настройка DI
# # app.dependency_overrides.update({
# #     animal_controller.Container.animal_repo: lambda: container.animal_repo(),
# #     animal_controller.Container.animal_transfer_service: lambda: container.animal_transfer_service(),
# # })


# app.dependency_overrides.update({
#     InMemoryAnimalRepository: container.animal_repo.provider,
#     AnimalTransferService: container.animal_transfer_service.provider,
# })

# app.include_router(animal_controller.router)
# # Инициализация шины событий
# event_bus = EventBus()

# # Пример обработчика для AnimalMovedEvent
# def log_animal_move(event):
#     print(f"Animal {event.animal_id} moved from {event.old_enclosure_id} to {event.new_enclosure_id}")

# event_bus.subscribe(animal_controller.AnimalMovedEvent, log_animal_move)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

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

# Регистрация контроллеров
app.include_router(animal_controller.router)
app.include_router(enclosure_controller.router)
app.include_router(feeding_controller.router)
app.include_router(stats_controller.router)

# Настройка DI через переопределения зависимостей
# app.dependency_overrides.update({
#     InMemoryAnimalRepository: get_animal_repo,
#     AnimalTransferService: get_transfer_service,
# })


app.dependency_overrides.update({
    InMemoryAnimalRepository: get_animal_repo,
    InMemoryEnclosureRepository: get_enclosure_repo,
    InMemoryFeedingScheduleRepository: get_feeding_repo,
    AnimalTransferService: get_transfer_service,
    FeedingOrganizationService: get_feeding_service,
    ZooStatisticsService: get_stats_service,
})

# Инициализация шины событий
event_bus = EventBus()

# Пример обработчика для AnimalMovedEvent
def log_animal_move(event):
    print(f"Animal {event.animal_id} moved from {event.old_enclosure_id} to {event.new_enclosure_id}")

event_bus.subscribe(AnimalMovedEvent, log_animal_move)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
