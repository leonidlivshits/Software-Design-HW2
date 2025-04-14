from domain.value_objects.EnclosureType import EnclosureType


class Species:
    COMPATIBLE_ENCLOSURE_TYPES = {
        "lion": "predator",
        "giraffe": "herbivore",
        "fish" : "aquarium", 
        "bat" : "aviary",
    }

    COMPATIBLE_FOOD = {
        "lion": "meat",
        "giraffe": "grass",
        "fish": "fish_food",
        "bat": "insects",
    }

    def __init__(self, name: str):
        if name not in self.COMPATIBLE_ENCLOSURE_TYPES:
            raise ValueError("Недопустимый вид животного")
        self.name = name
        self.compatible_enclosure_type = EnclosureType(
            self.COMPATIBLE_ENCLOSURE_TYPES[name]
        )
        self.food_type = self.COMPATIBLE_FOOD[name]