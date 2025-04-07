from domain.repositories.IAnimalRepository import IAnimalRepository


class InMemoryAnimalRepository(IAnimalRepository):
    def __init__(self):
        #self.counter = 0
        self.animals = {}

    def save(self, animal):
        #self.counter += 1
        self.animals[animal.id] = animal

    def get_by_id(self, animal_id):
        return self.animals.get(animal_id)

    def delete(self, animal_id):
        if animal_id in self.animals:
            del self.animals[animal_id]

    def get_all(self):
        return list(self.animals.values())