from domain.entities.Enclosure import Enclosure
from domain.repositories.IAnimalRepository import IAnimalRepository
from domain.repositories.IEnclosureRepository import IEnclosureRepository


class ZooStatisticsService:
    def __init__(
        self,
        animal_repo: IAnimalRepository,
        enclosure_repo: IEnclosureRepository
    ):
        self.animal_repo = animal_repo
        self.enclosure_repo = enclosure_repo

    def get_animal_count(self) -> int:
        return len(self.animal_repo.get_all())

    def get_free_enclosures(self) -> list[Enclosure]:
        return [
            enc for enc in self.enclosure_repo.get_all()
            if len(enc.current_animals) < enc.max_capacity
        ]