import pytest
from app import create_app
from app.models.user import User
from app.models.amenity import Amenity

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
def amenity_data():
    """Fixture providing test data for an amenity"""
    return {
        "name": "WiFi",
        "description": "High-speed wireless internet"
    }
