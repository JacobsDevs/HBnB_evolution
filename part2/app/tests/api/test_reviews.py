import pytest
from app.services.facade import facade

class TestReviews():
    def test_review_post(self, client, review_data):
        """Tests creating a review"""
        response = client.post("/api/v1/reviews/", json=review_data)

        assert response.status_code == 201
        assert 'id' in response.json
        assert response.json['text'] == 'Great place to stay!'

    def test_review_get_all(self, client, review_data):
        """Gets all reviews in the review_repo"""
        # Create a review first
        client.post("/api/v1/reviews/", json=review_data)

        response = client.get("/api/v1/reviews/")

        assert response.status_code == 200
        assert len(response.json) > 0
        assert any(r["text"] == "Great place to stay!" for r in response.json)

    def test_review_get_by_id(self, client, review_data):
        """Gets a review by ID"""
        # Create a review first
        post_response = client.post("/api/v1/reviews/", json=review_data)
        review_id = post_response.json['id']

        response = client.get(f"/api/v1/reviews/{review_id}")

        assert response.status_code == 200
        assert response.json["id"] == review_id
        assert response.json["text"] == "Great place to stay!"

    def test_review_update(self, client, review_data):
        """Updates a review"""
        # First create a review
        post_response = client.post("/api/v1/reviews/", json=review_data)
        review_id = post_response.json["id"]

        # Update the review
        update_data = {
            "text": "Even better than expected!",
            "rating": 5
        }
        response = client.put(f"/api/v1/reviews/{review_id}", json=update_data)

        # If the status code is not 200, print the response content for debugging
        if response.status_code != 200:
            print("Response status:", response.status_code)
            print("Response content:", response.json)

        assert response.status_code == 200
        assert response.json["text"] == "Even better than expected!"

    def test_review_delete(self, client, review_data):
        """Deletes a review"""
        # First create a review
        post_response = client.post("/api/v1/reviews/", json=review_data)
        review_id = post_response.json["id"]

        # Delete the review
        response = client.delete(f"/api/v1/reviews/{review_id}")
        assert response.status_code == 204

        # Verify the review was deleted
        get_response = client.get(f"/api/v1/reviews/{review_id}")
        assert get_response.status_code == 404
