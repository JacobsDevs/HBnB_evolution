import pytest
from app import create_app
from app.models.user import User
from app.models.amenity import Amenity


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
        "place_id": '',  # Use the actual place ID
        "user_id": ''     # Use the actual user ID
    }

@pytest.fixture()
def user():
  return {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@smith.com",
        "password": "abcd1234!"
    }

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
