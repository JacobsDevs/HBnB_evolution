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
def user(app):
    from app.models.user import User
    from app.services.facade import facade

    # Create a user
    new_user = User("John", "Smith", "john@smith.com", "abcd1234!")
    facade.user_repo.add(new_user)
    return new_user

@pytest.fixture()
def place(app, user):
    from app.models.place import Place
    from app.services.facade import facade

    # Create a place
    new_place = Place(
        title="Test Place",
        description="A nice place to stay",
        price=100.00,
        latitude=0.0,
        longitude=0.0,
        owner=user
    )
    facade.place_repo.add(new_place)
    return new_place

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
