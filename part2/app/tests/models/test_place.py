from app.models.place import Place
from app.models.user import User
# from app.models.review import Review
# from app.models.amenity import Amenity
# from app.services.facade import HBnBFacade

import pytest

class TestPlace():

    @pytest.fixture
    def valid_user(self):
        user = User("John", "Smith", "john@smith.com", "password")
        yield user


    @pytest.fixture
    def valid_place(self, valid_user):
        place = Place(
            title="Casa",
            description="Bonita",
            price=550.50,
            latitude=-37.81712,
            longitude=144.95926,
            owner_id=valid_user
            )
        yield place
    
    def test_place_instantiation(self, valid_place, valid_user):
        """
        Test that the Place object is created with valid attributes.
        """
        assert valid_place.title == "Cozy Apartment"
        assert valid_place.description == "A nice place to stay"
        assert valid_place.price == 100.0
        assert valid_place.latitude == 37.7749
        assert valid_place.longitude == -122.4194
        assert valid_place.owner == valid_user

    def test_place_title_missing(self, valid_user):
        """
        Title is required.
        """
        with pytest.raises(ValueError) as exception:
            place = Place(
                title="",
                description="A nice place to stay",
                price=100.0,
                latitude=37.7749,
                longitude=-122.4194,
                owner=valid_user
            )
        assert "Title is required" in str(exception.value)

    def test_place_title_too_long(self, valid_user):
        """
        Title must be less than 100 characters.
        """
        with pytest.raises(ValueError) as exception:
            place = Place(
                title="A" * 101,
                description="A nice place to stay",
                price=100.0,
                latitude=37.7749,
                longitude=-122.4194,
                owner=valid_user
            )
        assert "Title must be less than 100 characters" in str(exception.value)

    def test_place_price_negative(self, valid_user):
        """
        Price must be positive.
        """
        with pytest.raises(ValueError) as exception:
            place = Place(
                title="Cozy Apartment",
                description="A nice place to stay",
                price=-50.0,
                latitude=37.7749,
                longitude=-122.4194,
                owner=valid_user
            )
        assert "Price must be a positive value" in str(exception.value)

    def test_place_latitude_out_of_range(self, valid_user):
        """
        Latitude must be within -90 to 90.
        """
        with pytest.raises(ValueError) as exception:
            place = Place(
                title="Cozy Apartment",
                description="A nice place to stay",
                price=100.0,
                latitude=100.0,
                longitude=-122.4194,
                owner=valid_user
            )
        assert "Latitude must be between -90 and 90" in str(exception.value)

    def test_place_longitude_out_of_range(self, valid_user):
        """
        Longitude must be within -180 to 180.
        """
        with pytest.raises(ValueError) as exception:
            place = Place(
                title="Cozy Apartment",
                description="A nice place to stay",
                price=100.0,
                latitude=37.7749,
                longitude=200.0,
                owner=valid_user
            )
        assert "Longitude must be between -180 and 180" in str(exception.value)

    def test_place_owner_missing(self):
        """
        Owner is required.
        """
        with pytest.raises(ValueError) as exception:
            place = Place(
                title="Cozy Apartment",
                description="A nice place to stay",
                price=100.0,
                latitude=37.7749,
                longitude=-122.4194,
                owner=None
            )
        assert "Owner is required" in str(exception.value)

    
