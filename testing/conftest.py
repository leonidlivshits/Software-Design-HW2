# testing/conftest.py

import sys
import os

# Путь к корню проекта (два уровня выше testing/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import pytest

from application.services.animal_transfer_service import AnimalTransferService
from application.services.feeding_organization_service import FeedingOrganizationService
from application.services.zoo_statistics_service import ZooStatisticsService
from infrastructure.repositories.in_memory_animal_repository import InMemoryAnimalRepository
from infrastructure.repositories.in_memory_enclosure_repository import InMemoryEnclosureRepository
from infrastructure.repositories.in_memory_feeding_repository import InMemoryFeedingScheduleRepository


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