import pytest
from fastapi import status
from domain.entities.Animal import Animal
from domain.value_objects.Species import Species

class TestStatsController:
    def test_get_animal_stats(self, client, animal_repo):
        resp = client.get("/stats/animals")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json().get("total_animals") == 0

        a = Animal(
            id="1",
            species=Species("lion"),
            name="Leo",
            birth_date="2021-01-01",
            gender="male"
        )
        animal_repo.save(a)
        resp2 = client.get("/stats/animals")
        assert resp2.json().get("total_animals") == 1

    def test_get_free_enclosures(self, client, enclosure_repo):
        resp = client.get("/stats/enclosures/free")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json().get("free_enclosures") == 0

        from domain.value_objects.EnclosureType import EnclosureType
        from domain.entities.Enclosure import Enclosure
        e1 = Enclosure(id=None, enclosure_type=EnclosureType("predator"), max_capacity=2)
        e2 = Enclosure(id=None, enclosure_type=EnclosureType("herbivore"), max_capacity=3)
        enclosure_repo.save(e1)
        enclosure_repo.save(e2)
        resp2 = client.get("/stats/enclosures/free")
        assert resp2.json().get("free_enclosures") == 2
