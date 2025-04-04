from domain.events.AnimalMovedEvent import AnimalMovedEvent
from domain.repositories.IAnimalRepository import IAnimalRepository
from domain.repositories.IEnclosureRepository import IEnclosureRepository


class AnimalTransferService:
    def __init__(
        self,
        animal_repo: IAnimalRepository,
        enclosure_repo: IEnclosureRepository
    ):
        self.animal_repo = animal_repo
        self.enclosure_repo = enclosure_repo

    def move_animal(self, animal_id: str, new_enclosure_id: str) -> AnimalMovedEvent:
        animal = self.animal_repo.get_by_id(animal_id)
        new_enclosure = self.enclosure_repo.get_by_id(new_enclosure_id)
        old_enclosure = self.enclosure_repo.get_by_id(animal.enclosure_id)

        if not animal or not new_enclosure:
            raise ValueError("Объект не найден")

        # Проверки бизнес-правил
        if new_enclosure.type != animal.species.compatible_enclosure_type:
            raise ValueError("Тип вольера не совместим с видом животного")

        if len(new_enclosure.current_animals) >= new_enclosure.max_capacity:
            raise ValueError("Новый вольер переполнен")

        # Обновление данных
        if old_enclosure:
            old_enclosure.remove_animal(animal)
            self.enclosure_repo.save(old_enclosure)

        new_enclosure.add_animal(animal)
        self.enclosure_repo.save(new_enclosure)
        self.animal_repo.save(animal)

        # Генерация события
        return AnimalMovedEvent(
            animal_id=animal.id,
            old_enclosure_id=old_enclosure.id if old_enclosure else None,
            new_enclosure_id=new_enclosure.id
        )