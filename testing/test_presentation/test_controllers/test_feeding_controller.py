import pytest
from fastapi import status
from domain.entities.Animal import Animal
from domain.value_objects.Species import Species

class TestFeedingController:
    def test_create_feeding_schedule_success(self, client, saved_lion):
        resp = client.post(
            "/feeding-schedules/",
            params={
                "animal_id": saved_lion.id,
                "feeding_time_hour": 8,
                "feeding_time_minute": 30,
                "food_type": "ignored"
            }
        )
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.json()
        assert "id" in data and "event" in data

        all_schedules = client.get("/feeding-schedules/").json()
        assert any(sch.get("id") == data["id"] for sch in all_schedules)

    def test_create_feeding_schedule_invalid_animal(self, client):
        resp = client.post(
            "/feeding-schedules/",
            params={
                "animal_id": "999",
                "feeding_time_hour": 9,
                "feeding_time_minute": 0,
                "food_type": "ignored"
            }
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_all_schedules_and_get_by_id(self, client, saved_lion):
        for h in (7, 12):
            client.post(
                "/feeding-schedules/",
                params={"animal_id": saved_lion.id, "feeding_time_hour": h, "feeding_time_minute": 0, "food_type": "x"}
            )
        all_resp = client.get("/feeding-schedules/")
        assert all_resp.status_code == status.HTTP_200_OK
        schedules = all_resp.json()
        assert isinstance(schedules, list)
        assert len(schedules) >= 2

        sid = schedules[0].get("id")
        one = client.get(f"/feeding-schedules/{sid}")
        assert one.status_code == status.HTTP_200_OK
        assert one.json().get("id") == sid

    def test_get_schedule_not_found(self, client):
        resp = client.get("/feeding-schedules/999")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_mark_as_completed_success(self, client, saved_lion):
        c = client.post(
            "/feeding-schedules/",
            params={"animal_id": saved_lion.id, "feeding_time_hour": 10, "feeding_time_minute": 15, "food_type": "x"}
        )
        assert c.status_code == status.HTTP_201_CREATED
        sid = c.json().get("id")
        assert sid is not None

        comp = client.post(f"/feeding-schedules/{sid}/complete")
        assert comp.status_code == status.HTTP_200_OK
        assert comp.json().get("message") == "Schedule marked as completed"

        sch = client.get(f"/feeding-schedules/{sid}")
        assert sch.status_code == status.HTTP_200_OK
        data = sch.json()

        assert "is_completed" in data, f"Field 'is_completed' missing in response: {data}"
        assert data["is_completed"] is True

    def test_mark_as_completed_not_found(self, client):
        resp = client.post("/feeding-schedules/999/complete")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_mark_as_completed_feed_fail(self, client, saved_lion, animal_repo):
        saved_lion.is_healthy = False
        animal_repo.save(saved_lion)
        c = client.post(
            "/feeding-schedules/",
            params={"animal_id": saved_lion.id, "feeding_time_hour": 11, "feeding_time_minute": 45, "food_type": "x"}
        ).json()
        sid = c.get("id")
        comp = client.post(f"/feeding-schedules/{sid}/complete")
        assert comp.status_code == status.HTTP_400_BAD_REQUEST
        assert "Животное больно!" in comp.json().get("detail", "")