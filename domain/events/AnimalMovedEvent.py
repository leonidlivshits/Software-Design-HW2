class AnimalMovedEvent:
    def __init__(self, animal_id, old_enclosure_id, new_enclosure_id):
        self.animal_id = animal_id
        self.old_enclosure_id = old_enclosure_id
        self.new_enclosure_id = new_enclosure_id