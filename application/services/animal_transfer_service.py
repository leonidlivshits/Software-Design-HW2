from domain.events.AnimalMovedEvent import AnimalMovedEvent
from domain.repositories.IAnimalRepository import IAnimalRepository
from domain.repositories.IEnclosureRepository import IEnclosureRepository
import logging

logger = logging.getLogger(__name__)

class AnimalTransferService:
    def __init__(
        self,
        animal_repo: IAnimalRepository,
        enclosure_repo: IEnclosureRepository
    ):
        self.animal_repo = animal_repo
        self.enclosure_repo = enclosure_repo

    def move_animal(self, animal_id: str, new_enclosure_id: str) -> AnimalMovedEvent:
        try:
            logger.info(f"Поиск животного с ID={animal_id}")
            animal = self.animal_repo.get_by_id(animal_id)
            if not animal:
                raise ValueError("Животное не найдено")

            logger.info(f"Поиск нового вольера с ID={new_enclosure_id}")
            new_enclosure = self.enclosure_repo.get_by_id(new_enclosure_id)
            if not new_enclosure:
                raise ValueError("Новый вольер не найден")

            old_enclosure = None
            if animal.enclosure_id is not None:
                logger.info(f"Поиск старого вольера с ID={animal.enclosure_id}")
                old_enclosure = self.enclosure_repo.get_by_id(animal.enclosure_id)

            logger.info(
                f"Проверка совместимости: "
                f"Тип вольера={new_enclosure.type.type_name}, "
                f"Ожидаемый тип={animal.species.compatible_enclosure_type}"
            )
            if new_enclosure.type != animal.species.compatible_enclosure_type:
                raise ValueError("Тип вольера не совместим с видом животного")
            

            if len(new_enclosure.current_animals) >= new_enclosure.max_capacity:
                raise ValueError("Новый вольер переполнен")

            if old_enclosure:
                logger.info(f"Удаление животного из старого вольера {old_enclosure.id}")
                old_enclosure.remove_animal(animal)
                self.enclosure_repo.save(old_enclosure)

            logger.info(f"Добавление животного в новый вольер {new_enclosure.id}")
            new_enclosure.add_animal(animal)
            self.enclosure_repo.save(new_enclosure)

            animal.enclosure_id = new_enclosure.id
            self.animal_repo.save(animal)

            event = AnimalMovedEvent(
                animal_id=animal.id,
                old_enclosure_id=old_enclosure.id if old_enclosure else None,
                new_enclosure_id=new_enclosure.id
            )
            logger.info(f"Событие перемещения: {event}")
            return event

        except Exception as e:
            logger.error(f"Ошибка при перемещении животного: {str(e)}", exc_info=True)
            raise