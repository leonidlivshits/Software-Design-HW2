from __future__ import annotations
from typing import TYPE_CHECKING
from domain.value_objects import Species

if TYPE_CHECKING:
    from domain.entities.Enclosure import Enclosure

class Animal:
    def __init__(
        self,
        id: str,
        species: Species,
        name: str,
        birth_date: str,
        gender: str,
        favorite_food: str,
        is_healthy: bool = True
    ):
        self.id = id
        self.species = species
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.favorite_food = favorite_food
        self.is_healthy = is_healthy
        self.enclosure_id = None

    def move(self, new_enclosure: Enclosure) -> None:  # Используем аннотацию как строку
        if new_enclosure.type != self.species.compatible_enclosure_type:
            raise ValueError("Тип вольера не совместим с видом животного")
        self.enclosure_id = new_enclosure.id

    def feed(self, food_type: str) -> None:
        if food_type != self.favorite_food:
            raise ValueError("Животное отказывается есть эту пищу")
        # Дополнительная логика (например, обновление статуса)
        if not self.is_healthy:
            self.is_healthy = True  # Выздоровление после кормления

    def heal(self) -> None:
        self.is_healthy = True
