import pytest
from unittest.mock import patch

from padel_discovery.core.models import Coach, Court, SearchLog, Tournament


@pytest.fixture
def search_data(db):
    Court.objects.create(
        name="Budget Court",
        address="Address",
        city="Bangalore",
        state="Karnataka",
        latitude=12.9,
        longitude=77.5,
        hourly_price=700,
        phone="123",
        website="https://example.com",
        google_rating=4.4,
        description="Budget and beginner friendly",
    )
    Court.objects.create(
        name="Premium Court",
        address="Address",
        city="Mumbai",
        state="Maharashtra",
        latitude=19.0,
        longitude=72.8,
        hourly_price=1200,
        phone="123",
        website="https://example.com",
        google_rating=4.8,
        description="Premium",
    )
    Coach.objects.create(
        name="Budget Coach",
        city="Bangalore",
        experience_years=4,
        specialties="beginner, fitness",
        phone="123",
        bio="Helpful beginner coach",
        verified=True,
    )
    Tournament.objects.create(
        title="Weekend Cup",
        city="Bangalore",
        venue="Venue",
        date="2026-07-01",
        entry_fee=2000,
        description="Weekend event",
        registration_url="https://example.com/register",
    )


@pytest.mark.django_db
@patch("padel_discovery.core.views.gemini_filters", return_value={"city": "Bangalore", "max_price": 800, "category": "courts", "text": "Courts in Bangalore under 800"})
def test_search_courts(mock_filters, api_client, search_data):
    response = api_client.post("/api/search/", {"query": "Courts in Bangalore under 800"}, format="json")
    assert response.status_code == 200
    assert len(response.data["courts"]) == 1
    assert response.data["courts"][0]["name"] == "Budget Court"
    assert response.data["coaches"] == []
    assert response.data["tournaments"] == []
    assert SearchLog.objects.count() == 1


@pytest.mark.django_db
@patch("padel_discovery.core.views.gemini_filters", return_value={"city": "Bangalore", "category": "coaches", "text": "Good coaches near Bangalore"})
def test_search_coaches(mock_filters, api_client, search_data):
    response = api_client.post("/api/search/", {"query": "Good coaches near Bangalore"}, format="json")
    assert response.status_code == 200
    assert len(response.data["coaches"]) == 1
    assert response.data["coaches"][0]["name"] == "Budget Coach"
