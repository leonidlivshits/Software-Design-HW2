class EnclosureType:
    VALID_TYPES = ["predator", "herbivore", "aquarium", "aviary"]

    def __init__(self, type_name: str):
        if type_name not in self.VALID_TYPES:
            raise ValueError("Недопустимый тип вольера")
        self.type_name = type_name

    def __eq__(self, other):
        if isinstance(other, EnclosureType):
            return self.type_name == other.type_name
        return False

    def __repr__(self):
        return f"EnclosureType(type_name='{self.type_name}')"