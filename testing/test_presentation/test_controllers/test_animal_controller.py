from fastapi import status

class TestAnimalController:
    def test_create_animal_success(self, client, animal_repo, sample_animal_data):
        response = client.post("/animals/", params=sample_animal_data)
        assert response.status_code == status.HTTP_201_CREATED
        animals = animal_repo.get_all()
        assert len(animals) == 1
        assert animals[0].name == sample_animal_data["name"]

    def test_get_all_animals(self, client, saved_lion):
        response = client.get("/animals/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == saved_lion.name

    def test_delete_animal_success(self, client, saved_lion, animal_repo):
        assert animal_repo.get_by_id(saved_lion.id) is not None
        
        response = client.delete(f"/animals/{saved_lion.id}")
        assert response.status_code == status.HTTP_200_OK
        assert animal_repo.get_by_id(saved_lion.id) is None

    def test_heal_animal_success(self, client, saved_lion, animal_repo):

        saved_lion.is_healthy = False
        animal_repo.save(saved_lion)
        
        response = client.post(f"/animals/{saved_lion.id}/heal")
        assert response.status_code == status.HTTP_200_OK
        assert animal_repo.get_by_id(saved_lion.id).is_healthy is True

    def test_move_animal_success(self, client, saved_lion, predator_enclosure):
        saved_lion.enclosure_id = "temp"
        response = client.post(
            f"/animals/{saved_lion.id}/move",
            params={"new_enclosure_id": predator_enclosure.id}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_move_animal_invalid_enclosure(
        self, 
        client, 
        saved_lion, 
        herbivore_enclosure,
        enclosure_repo
    ):
        from domain.entities.Enclosure import Enclosure
        from domain.value_objects.EnclosureType import EnclosureType
        enclosure = herbivore_enclosure
        enclosure_repo.save(enclosure)
        
        response = client.post(
            f"/animals/{saved_lion.id}/move",
            params={"new_enclosure_id": "2"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST