import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from padel_discovery.core.models import Coach, Court, Tournament


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def seeded_data(db):
    Court.objects.create(
        name="Court 1",
        address="Address",
        city="Bangalore",
        state="Karnataka",
        latitude=12.9,
        longitude=77.5,
        hourly_price=750,
        phone="123",
        website="https://example.com",
        google_rating=4.5,
        description="Beginner friendly",
    )
    Coach.objects.create(
        name="Coach 1",
        city="Bangalore",
        experience_years=7,
        specialties="beginner, fitness",
        phone="123",
        bio="Bio",
        verified=True,
    )
    Tournament.objects.create(
        title="Tournament 1",
        city="Bangalore",
        venue="Venue",
        date="2026-07-01",
        entry_fee=1000,
        description="Desc",
        registration_url="https://example.com/register",
    )


@pytest.mark.django_db
def test_list_endpoints(api_client, seeded_data):
    assert api_client.get("/api/courts/").status_code == 200
    assert api_client.get("/api/coaches/").status_code == 200
    assert api_client.get("/api/tournaments/").status_code == 200


@pytest.mark.django_db
def test_detail_endpoints(api_client, seeded_data):
    court = Court.objects.first()
    coach = Coach.objects.first()
    tournament = Tournament.objects.first()

    assert api_client.get(f"/api/courts/{court.id}/").status_code == 200
    assert api_client.get(f"/api/coaches/{coach.id}/").status_code == 200
    assert api_client.get(f"/api/tournaments/{tournament.id}/").status_code == 200


@pytest.mark.django_db
def test_login_and_refresh(api_client, db):
    get_user_model().objects.create_user(username="admin", password="secret12345")
    response = api_client.post("/api/auth/login/", {"username": "admin", "password": "secret12345"}, format="json")
    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None

    refresh_response = api_client.post("/api/auth/refresh/", {}, format="json")
    assert refresh_response.status_code == 200


@pytest.mark.django_db
def test_schema_endpoint(api_client):
    assert api_client.get("/api/schema/").status_code == 200
