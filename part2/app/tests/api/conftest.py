import pytest
from app import create_app
from app.models.user import User


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def user():
    return User("John", "Smith", "john@smith.com", "abcd1234!")

@pytest.fixture()
def place():
    place = {
        "title": "Holberton",
        "description": "Melbourne School",
        "price": 100,
        "latitude": -37.81712,
        "longitude": 144.95926,
        "owner_id": "12345",
        "amenities": [],
    }
    return place

@pytest.fixture()
def update():
    new_place = {
        "title": "KameHouse",
        "price": 10.10,
        "latitude": 20.20,
        "longitude": 30.30,
        "owner_id": "56789",
        "amenities": [],
    }
    return new_place