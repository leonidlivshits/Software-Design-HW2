from __future__ import annotations
from typing import TYPE_CHECKING
from domain.value_objects import EnclosureType

if TYPE_CHECKING:
    from domain.entities.Animal import Animal

class Enclosure:
    def __init__(
        self,
        id: str,
        enclosure_type: EnclosureType,
        max_capacity: int
    ):
        self.id = id
        self.type = enclosure_type
        self.max_capacity = max_capacity
        self.current_animals = []

    def add_animal(self, animal: Animal) -> None:
        if len(self.current_animals) >= self.max_capacity:
            raise ValueError("Вольер переполнен")
        if animal.species.compatible_enclosure_type != self.type:
            raise ValueError("Несовместимый тип вольера")
        if animal.id in self.current_animals:
            raise ValueError("Животное уже находится в этом вольере")
        
        self.current_animals.append(animal.id)
        animal.enclosure_id = self.id


    def remove_animal(self, animal: Animal) -> None:
        if animal.id not in self.current_animals:
            raise ValueError("Животное не находится в этом вольере")
        self.current_animals.remove(animal.id)
        animal.enclosure_id = None