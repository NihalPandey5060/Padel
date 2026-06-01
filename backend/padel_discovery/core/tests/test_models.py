import pytest

from padel_discovery.core.models import Coach, Court, Tournament


@pytest.mark.django_db
def test_models_string_representations():
    court = Court.objects.create(
        name="Test Court",
        address="Address",
        city="Bangalore",
        state="Karnataka",
        latitude=12.9,
        longitude=77.5,
        hourly_price=500,
        phone="123",
        website="https://example.com",
        google_rating=4.5,
        description="Nice court",
    )
    coach = Coach.objects.create(
        name="Test Coach",
        city="Mumbai",
        experience_years=5,
        specialties="beginner, fitness",
        phone="123",
        bio="Bio",
        verified=True,
    )
    tournament = Tournament.objects.create(
        title="Test Tournament",
        city="Delhi",
        venue="Venue",
        date="2026-07-01",
        entry_fee=1000,
        description="Desc",
        registration_url="https://example.com/register",
    )

    assert str(court) == "Test Court (Bangalore)"
    assert str(coach) == "Test Coach (Mumbai)"
    assert str(tournament) == "Test Tournament (Delhi)"
