from domain.value_objects.EnclosureType import EnclosureType


class Species:
    COMPATIBLE_ENCLOSURE_TYPES = {
        "lion": "predator",
        "giraffe": "herbivore",
        "fish" : "aquarium", 
        "bat" : "aviary",
    }

    def __init__(self, name: str):
        if name not in self.COMPATIBLE_ENCLOSURE_TYPES:
            raise ValueError("Недопустимый вид животного")
        self.name = name
        self.compatible_enclosure_type = EnclosureType(
            self.COMPATIBLE_ENCLOSURE_TYPES[name]
        )