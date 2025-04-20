import pytest
from fastapi import status
from domain.entities.Animal import Animal
from domain.value_objects.Species import Species

class TestEnclosureController:
    def test_create_enclosure_success(self, client, enclosure_repo):
        response = client.post(
            "/enclosures/",
            params={"enclosure_type": "predator", "max_capacity": 5}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data and "type" in data
        assert data["type"] == "predator"
        assert len(enclosure_repo.get_all()) == 1

    def test_create_enclosure_invalid_type(self, client):
        response = client.post(
            "/enclosures/",
            params={"enclosure_type": "invalid", "max_capacity": 5}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Недопустимый тип вольера" in response.json()["detail"]

    def test_get_all_enclosures(self, client, predator_enclosure):
        response = client.get("/enclosures/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert any(e.get("id") == predator_enclosure.id for e in data)

    def test_get_enclosure_by_id_success(self, client, predator_enclosure):
        response = client.get(f"/enclosures/{predator_enclosure.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == predator_enclosure.id
        assert data["type"]["type_name"] == predator_enclosure.type.type_name
        assert data["max_capacity"] == predator_enclosure.max_capacity
        assert isinstance(data["current_animals"], list)

    def test_get_enclosure_not_found(self, client):
        response = client.get("/enclosures/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_enclosure_success(self, client, predator_enclosure, enclosure_repo):
        response = client.delete(f"/enclosures/{predator_enclosure.id}")
        assert response.status_code == status.HTTP_200_OK
        assert enclosure_repo.get_by_id(predator_enclosure.id) is None

    def test_delete_enclosure_not_found(self, client):
        response = client.delete("/enclosures/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_add_animal_success(self, client, saved_lion, predator_enclosure):
        response = client.post(
            f"/enclosures/{predator_enclosure.id}/add_animal",
            params={"animal_id": saved_lion.id}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Animal added to enclosure"

        get_resp = client.get(f"/enclosures/{predator_enclosure.id}")
        encl = get_resp.json()
        assert any(saved_lion.id in a for a in encl["current_animals"])

    def test_add_animal_invalid_enclosure(self, client, saved_lion):
        response = client.post(
            "/enclosures/999/add_animal",
            params={"animal_id": saved_lion.id}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_add_animal_invalid_animal(self, client, predator_enclosure):
        response = client.post(
            f"/enclosures/{predator_enclosure.id}/add_animal",
            params={"animal_id": "999"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_add_animal_already_in_other_enclosure(
        self,
        client,
        saved_lion,
        predator_enclosure,
        herbivore_enclosure
    ):
        
        client.post(
            f"/enclosures/{predator_enclosure.id}/add_animal",
            params={"animal_id": saved_lion.id}
        )

        response = client.post(
            f"/enclosures/{herbivore_enclosure.id}/add_animal",
            params={"animal_id": saved_lion.id}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Животное уже находится в другом вольере" in response.json()["detail"]

    def test_remove_animal_success(self, client, saved_lion, predator_enclosure):
        client.post(
            f"/enclosures/{predator_enclosure.id}/add_animal",
            params={"animal_id": saved_lion.id}
        )
        response = client.post(
            f"/enclosures/{predator_enclosure.id}/remove_animal",
            params={"animal_id": saved_lion.id}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Animal removed from enclosure"

        get_resp = client.get(f"/enclosures/{predator_enclosure.id}")
        assert all(a != saved_lion.id for a in get_resp.json()["current_animals"])

    def test_remove_animal_not_found_enclosure(self, client, saved_lion):
        response = client.post(
            "/enclosures/999/remove_animal",
            params={"animal_id": saved_lion.id}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_remove_animal_not_found_animal(self, client, predator_enclosure):
        response = client.post(
            f"/enclosures/{predator_enclosure.id}/remove_animal",
            params={"animal_id": "999"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_remove_animal_not_in_enclosure(self, client, saved_lion, predator_enclosure):
        response = client.post(
            f"/enclosures/{predator_enclosure.id}/remove_animal",
            params={"animal_id": saved_lion.id}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
