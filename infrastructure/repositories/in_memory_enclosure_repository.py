from domain.repositories.IEnclosureRepository import IEnclosureRepository


class InMemoryEnclosureRepository(IEnclosureRepository):
    def __init__(self):
        self.enclosures = {}

    def save(self, enclosure):
        self.enclosures[enclosure.id] = enclosure

    def get_by_id(self, enclosure_id):
        return self.enclosures.get(enclosure_id)

    def get_all(self):
        return list(self.enclosures.values())