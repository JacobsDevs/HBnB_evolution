import pytest
from part3.app import create_app
from part3.app.models.user import User
from part3.app.models.amenity import Amenity


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
def amenity_data():
    """Fixture providing test data for an amenity"""
    return {
        "name": "WiFi",
        "description": "High-speed wireless internet"
    }

@pytest.fixture()
def review_data(user, place):
    """Test data for a review"""
    return {
        "text": "Great place to stay!",
        "rating": 5,
        "place_id": place.id,  # Use the actual place ID
        "user_id": user.id     # Use the actual user ID
    }

@pytest.fixture()
def user():
    user = User("John", "Smith", "Johnny_smith@email.com", "G00dP455!")
    return user

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
