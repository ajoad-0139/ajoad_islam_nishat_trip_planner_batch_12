import pytest

from config import Config
from create_app import create_app

TRIP = {
    "destination": "Cox's Bazar",
    "start_date": "2026-10-20",
    "end_date": "2026-10-23",
    "budget": 1000,
    "max_travelers": 1,
}


@pytest.fixture()
def client():

    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

    return create_app(TestConfig).test_client()


def make_trip(client):
    response = client.post("/api/v1/trips", json=TRIP)
    assert response.status_code == 201
    return response.get_json()


# GET /health
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


# GET /api/v1/trips
def test_create_and_get_trip(client):
    trip = make_trip(client)
    assert trip["status"] == "PLANNED"

    response = client.get(f"/api/v1/trips/{trip['id']}")
    assert response.status_code == 200
    assert response.get_json()["destination"] == "Cox's Bazar"


def test_invalid_trip_rejected(client):
    bad = {**TRIP, "end_date": "2026-10-19"} 
    assert client.post("/api/v1/trips", json=bad).status_code == 400


# POST /api/v1/trips/<id>/travelers
def test_duplicate_traveler_and_capacity(client):
    trip = make_trip(client) 
    url = f"/api/v1/trips/{trip['id']}/travelers"
    person = {"name": "Ayesha Rahman", "email": "ayesha@example.com"}

    assert client.post(url, json=person).status_code == 201  
    assert client.post(url, json=person).status_code == 409 
    other = {"name": "Karim", "email": "karim@example.com"}
    assert client.post(url, json=other).status_code == 409 


# POST /api/v1/trips/<id>/expenses
def test_expense_budget_boundary(client):
    trip = make_trip(client) 
    url = f"/api/v1/trips/{trip['id']}/expenses"

    assert client.post(url, json={"title": "Hotel", "amount": 600}).status_code == 201
    assert client.post(url, json={"title": "Food", "amount": 400}).status_code == 201 
    assert client.post(url, json={"title": "Extra", "amount": 1}).status_code == 409 