import pytest
from part3.app.models.amenity import Amenity
from part3.app.services import facade

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

    def test_amenity_get_by_id(self, client, amenity_data):
        """Gets an amenity by ID"""
        # First create an amenity
        post_response = client.post("/api/v1/amenities/", json=amenity_data)
        amenity_id = post_response.json["id"]

        # Get the amenity by ID
        response = client.get(f"/api/v1/amenities/{amenity_id}")
        assert response.status_code == 200
        assert response.json["id"] == amenity_id
        assert response.json["name"] == "WiFi"

    def test_amenity_delete(self, client, amenity_data):
        """Deletes an amenity"""
        # First create an amenity
        post_response = client.post("/api/v1/amenities/", json=amenity_data)
        amenity_id = post_response.json["id"]

        # Delete the amenity
        response = client.delete(f"/api/v1/amenities/{amenity_id}")
        assert response.status_code == 204

        # Verify the amenity was deleted
        get_response = client.get(f"/api/v1/amenities/{amenity_id}")
        assert get_response.status_code == 404

    def test_amenity_update(self, client, amenity_data):
        """Updates an amenity"""
        # First create an amenity
        post_response = client.post("/api/v1/amenities/", json=amenity_data)
        amenity_id = post_response.json["id"]

        # Update the amenity - now including all original data
        update_data = {
            "name": "Free WiFi",
            "description": "Complimentary high-speed internet"
        }
        response = client.put(f"/api/v1/amenities/{amenity_id}", json=update_data)

        assert response.status_code == 200
        assert response.json["name"] == "Free WiFi"
        assert response.json["description"] == "Complimentary high-speed internet"

        # Verify the update was persisted
        get_response = client.get(f"/api/v1/amenities/{amenity_id}")
        assert get_response.json["name"] == "Free WiFi"
