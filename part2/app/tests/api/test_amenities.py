import pytest
from app.models.amenity import Amenity
from app.services import facade

class TestAmenities():
    def test_amenity_post(self, client, amenity_data):
        """Creates an amenity from posted json data"""
        response = client.post("/api/v1/amenities/", json=amenity_data)
        assert response.status_code == 201
        assert response.json["name"] == "WiFi"
        assert response.json["description"] == "High-speed wireless internet"
