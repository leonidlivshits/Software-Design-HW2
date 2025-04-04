class EnclosureType:
    VALID_TYPES = ["predator", "herbivore", "aquarium", "aviary"]

    def __init__(self, type_name: str):
        if type_name not in self.VALID_TYPES:
            raise ValueError("Недопустимый тип вольера")
        self.type_name = type_name