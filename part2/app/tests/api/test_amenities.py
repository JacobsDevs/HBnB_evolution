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

    def test_amenity_get_all(self, client, amenity_data):
        """Gets all amenities in the amenity_repo"""
        # First create an amenity
        client.post("/api/v1/amenities/", json=amenity_data)

        # Get all amenities
        response = client.get("/api/v1/amenities/")
        assert response.status_code == 200
        # Check that at least one amenity exists
        assert len(response.json) > 0
        # Check that our amenity is in the list
        assert any(a["name"] == "WiFi" for a in response.json)
