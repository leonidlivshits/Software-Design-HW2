import sys
import os



PROJECT_ROOT = os.getcwd()
sys.path.insert(0, PROJECT_ROOT)

# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from presentation.controllers.animal_controller import router as animal_router
from presentation.controllers.enclosure_controller import router as enclosure_router
from presentation.controllers.feeding_controller import router as feeding_router
from presentation.controllers.stats_controller   import router as stats_router
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from application.services.animal_transfer_service import AnimalTransferService
from application.services.feeding_organization_service import FeedingOrganizationService
from application.services.zoo_statistics_service import ZooStatisticsService
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from infrastructure.repositories.in_memory_enclosure_repository import InMemoryEnclosureRepository
from infrastructure.repositories.in_memory_feeding_repository import InMemoryFeedingScheduleRepository

from domain.entities.Animal import Animal
from domain.entities.Enclosure import Enclosure
from domain.value_objects.EnclosureType import EnclosureType
from domain.value_objects.Species import Species

from presentation.container import get_animal_repo, get_enclosure_repo, get_feeding_service, get_stats_service, get_transfer_service, get_feeding_repo

@pytest.fixture
def animal_repo():
    return InMemoryAnimalRepository()

@pytest.fixture
def enclosure_repo():
    return InMemoryEnclosureRepository()

@pytest.fixture
def feeding_repo():
    return InMemoryFeedingScheduleRepository()

@pytest.fixture
def transfer_service(animal_repo, enclosure_repo):
    return AnimalTransferService(animal_repo, enclosure_repo)

@pytest.fixture
def feeding_service(animal_repo, feeding_repo):
    return FeedingOrganizationService(animal_repo, feeding_repo)

@pytest.fixture
def stats_service(animal_repo, enclosure_repo):
    return ZooStatisticsService(animal_repo, enclosure_repo)

@pytest.fixture
def client(animal_repo, enclosure_repo, feeding_repo):
    app = FastAPI()
    app.include_router(animal_router)
    app.include_router(enclosure_router)
    app.include_router(feeding_router)
    app.include_router(stats_router)

    app.dependency_overrides[get_animal_repo] = lambda: animal_repo
    app.dependency_overrides[get_enclosure_repo] = lambda: enclosure_repo
    app.dependency_overrides[get_transfer_service] = (
    lambda: AnimalTransferService(animal_repo, enclosure_repo)
    )


    app.dependency_overrides[get_feeding_repo]    = lambda: feeding_repo
    app.dependency_overrides[get_feeding_service] = lambda: FeedingOrganizationService(animal_repo, feeding_repo)


    app.dependency_overrides[get_stats_service]   = lambda: ZooStatisticsService(animal_repo, enclosure_repo)
    return TestClient(app)

@pytest.fixture
def sample_animal_data():
    return {
        "species": "lion",
        "name": "Simba",
        "birth_date": "2020-01-01",
        "gender": "male"
    }

@pytest.fixture
def saved_lion(animal_repo, sample_animal_data):
    animal = Animal(
        id="1",
        species=Species(sample_animal_data["species"]),
        name=sample_animal_data["name"],
        birth_date=sample_animal_data["birth_date"],
        gender=sample_animal_data["gender"]
    )
    animal_repo.save(animal)
    return animal

@pytest.fixture
def predator_enclosure(enclosure_repo):
    enclosure = Enclosure(
        id="1",
        enclosure_type=EnclosureType("predator"),
        max_capacity=5
    )
    enclosure_repo.save(enclosure)
    return enclosure

@pytest.fixture
def herbivore_enclosure(enclosure_repo):
    enclosure = Enclosure(
            id="2",
            enclosure_type=EnclosureType("herbivore"),
            max_capacity=5
        )
    enclosure_repo.save(enclosure)
    return enclosure
    