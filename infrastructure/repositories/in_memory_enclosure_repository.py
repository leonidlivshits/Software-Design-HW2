
from domain.repositories.IEnclosureRepository import IEnclosureRepository

import logging

logger = logging.getLogger(__name__)

class InMemoryEnclosureRepository(IEnclosureRepository):
    def __init__(self):
        self.enclosures = {}
        self.counter = 0

    def save(self, enclosure):
        # Если вольер уже имеет ID — обновляем, иначе создаем новый
        if enclosure.id is None:
            self.counter += 1
            enclosure.id = str(self.counter)
        self.enclosures[enclosure.id] = enclosure
        logger.info(f"Сохранен вольер ID={enclosure.id} (всего: {len(self.enclosures)})")

    def get_by_id(self, enclosure_id):
        logger.info(f"Поиск вольера ID={enclosure_id}")
        return self.enclosures.get(enclosure_id)
    
    def get_all(self):
        return list(self.enclosures.values())