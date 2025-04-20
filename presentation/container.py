
# from dependency_injector import containers, providers

# from application.services.animal_transfer_service import AnimalTransferService
# from application.services.feeding_organization_service import FeedingOrganizationService
# from application.services.zoo_statistics_service import ZooStatisticsService
# from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
# from infrastructure.repositories.in_memory_enclosure_repository import InMemoryEnclosureRepository
# from infrastructure.repositories.in_memory_feeding_repository import InMemoryFeedingScheduleRepository



# class Container(containers.DeclarativeContainer):
#     animal_repo = providers.Singleton(InMemoryAnimalRepository)
#     enclosure_repo = providers.Singleton(InMemoryEnclosureRepository)
#     feeding_repo = providers.Singleton(InMemoryFeedingScheduleRepository)
    
#     # Сервисы (Factory)
#     animal_transfer_service = providers.Factory(
#         AnimalTransferService,
#         animal_repo=animal_repo,
#         enclosure_repo=enclosure_repo
#     )

    
#     feeding_service = providers.Factory(
#         FeedingOrganizationService,
#         animal_repo=animal_repo,
#         feeding_repo=feeding_repo
#     )
    
#     stats_service = providers.Factory(
#         ZooStatisticsService,
#         animal_repo=animal_repo,
#         enclosure_repo=enclosure_repo
#     )

#     # FastAPI-совместимые зависимости
#     def get_animal_repo(self) -> InMemoryAnimalRepository:
#         return self.animal_repo()
    
#     def get_enclosure_repo(self) -> InMemoryEnclosureRepository:
#         return self.enclosure_repo()
    
#     def get_transfer_service(self) -> AnimalTransferService:
#         return self.animal_transfer_service()

from dependency_injector import containers, providers

from application.services.animal_transfer_service import AnimalTransferService
from application.services.feeding_organization_service import FeedingOrganizationService
from application.services.zoo_statistics_service import ZooStatisticsService
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from infrastructure.repositories.in_memory_enclosure_repository import InMemoryEnclosureRepository
from infrastructure.repositories.in_memory_feeding_repository import InMemoryFeedingScheduleRepository


class Container(containers.DeclarativeContainer):
    animal_repo = providers.Singleton(InMemoryAnimalRepository)
    enclosure_repo = providers.Singleton(InMemoryEnclosureRepository)
    feeding_repo = providers.Singleton(InMemoryFeedingScheduleRepository)
    
    # Factory
    animal_transfer_service = providers.Factory(
        AnimalTransferService,
        animal_repo=animal_repo,
        enclosure_repo=enclosure_repo
    )

    feeding_service = providers.Factory(
        FeedingOrganizationService,
        animal_repo=animal_repo,
        feeding_repo=feeding_repo
    )
    
    stats_service = providers.Factory(
        ZooStatisticsService,
        animal_repo=animal_repo,
        enclosure_repo=enclosure_repo
    )


container = Container()

def get_animal_repo() -> InMemoryAnimalRepository:
    return container.animal_repo()

def get_transfer_service() -> AnimalTransferService:
    return container.animal_transfer_service()

def get_enclosure_repo() -> InMemoryEnclosureRepository:
    return container.enclosure_repo()

def get_feeding_repo() -> InMemoryFeedingScheduleRepository:
    return container.feeding_repo()

def get_feeding_service() -> FeedingOrganizationService:
    return container.feeding_service()

def get_stats_service() -> ZooStatisticsService:
    return container.stats_service()

    