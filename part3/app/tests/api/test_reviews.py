import pytest
from part3.app.services.facade import facade

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

    def test_get_reviews_for_place(self, client, review_data):
        """Tests retrieving reviews for a specific place"""
        # First create a review
        post_response = client.post("/api/v1/reviews/", json=review_data)
        place_id = review_data['place_id']
        
        # Get reviews for the place
        response = client.get(f"/api/v1/places/{place_id}/reviews")
        
        assert response.status_code == 200
        assert len(response.json) > 0
        
        # Check that our review is in the list
        review_texts = [r["text"] for r in response.json]
        assert "Great place to stay!" in review_texts
        
    def test_add_review_to_place(self, client, review_data):
        """Tests adding a review directly to a place"""
        place_id = review_data['place_id']
        
        # Create a new review for the place
        new_review_data = {
            "text": "Another excellent stay!",
            "rating": 4,
            "user_id": review_data['user_id']
        }
        
        response = client.post(f"/api/v1/places/{place_id}/reviews", json=new_review_data)
        
        assert response.status_code == 201
        assert response.json['text'] == "Another excellent stay!"
        assert response.json['place_id'] == place_id
        
        # Check that the review was added to the place
        get_response = client.get(f"/api/v1/places/{place_id}")
        reviews = get_response.json.get('reviews', [])
        
        review_texts = [r["text"] for r in reviews]
        assert "Another excellent stay!" in review_texts