class AnimalMovedEvent:
    def __init__(self, animal_id: str, old_enclosure_id: str, new_enclosure_id: str):
        self.animal_id = animal_id
        self.old_enclosure_id = old_enclosure_id
        self.new_enclosure_id = new_enclosure_id