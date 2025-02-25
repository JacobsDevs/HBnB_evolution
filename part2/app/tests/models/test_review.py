import pytest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.services.facade import HBnBFacade


class TestClass():
    """Test class for Review model"""

    def test_review_documentation(self):
        """
        Tests that the Review class and its methods have docstrings.
        This ensures that the code is properly documented.
        """
        # Check class docstring
        assert Review.__doc__ is not None
        assert len(Review.__doc__) > 0

        # Check method docstrings
        assert Review.__init__.__doc__ is not None
        assert Review.create.__doc__ is not None
        assert Review.update.__doc__ is not None
        assert Review.delete.__doc__ is not None
        assert Review.list_by_place.__doc__ is not None

    @pytest.fixture
    def valid_user(self):
        """
        This fixture creates a valid User instance for testing.
        
        The Review model requires a User instance for the reviewer attribute,
        so we need to create a valid User first.
        """
        user = User("John", "Smith", "john@smith.com", "password123")
        yield user

    @pytest.fixture
    def valid_place(self, valid_user):
        """
        This fixture creates a valid Place instance for testing.
        
        The Review model requires a Place instance for the place attribute,
        so we need to create a valid Place first.
        
        Note that this fixture depends on the valid_user fixture because
        a Place requires an owner (User).
        """
        place = Place(
                title="Cozy Apartment",
                description="A beautiful place in the city",
                price=100.50,
                latitude=37.7749,
                longitude=-122.4194,
                owner=valid_user
            )
        yield place

    @pytest.fixture
    def valid_review(self, valid_place, valid_user):
        """
        This fixture creates a valid Review instance for testing.
        
        According to the class diagram, Review should have:
        - reviewer (User)
        - place (Place)
        - rating (int)
        - comment (string) - called 'text' in the implementation
        - Inherited attributes from BaseEntity (id, created_at, updated_at)
        
        This fixture depends on both valid_place and valid_user fixtures.
        """
        review = Review(
                text="Great place, highly recommended!",
                rating=5,
                place=valid_place,
                user=valid_user
            )
        yield review

    @pytest.fixture
    def setup_facade(self, valid_user, valid_place, valid_review):
        """
        This fixture sets up the facade pattern with repositories containing
        the valid user, place, and review.
        
        It demonstrates the integration between the Review model and the
        facade/repository pattern required by the project.
        """
        facade = HBnBFacade()
        facade.user_repo.add(valid_user)
        facade.place_repo.add(valid_place)
        facade.review_repo.add(valid_review)
        yield facade.review_repo

    def test_fixtures_persist(self, setup_facade, valid_review):
        """
        Tests that the valid_review object is stored in the facade's review_repo.
        
        This verifies the basic functionality of the InMemoryRepository and its
        interaction with the Review model.
        """
        assert setup_facade.get_all() == [valid_review]

    def test_review_instantiation(self, valid_review, valid_place, valid_user):
        """
        Test basic review creation with all required attributes.
        
        This verifies that:
        1. The Review constructor works correctly
        2. All attributes are set properly
        3. The inheritance from BaseEntity provides id, created_at, and updated_at
        """
        review = valid_review
        assert review.text == "Great place, highly recommended!"
        assert review.rating == 5
        assert review.place == valid_place
        assert review.user == valid_user

        # Verify inherited attributes from BaseEntity
        assert hasattr(review, "id")
        assert hasattr(review, "created_at")
        assert hasattr(review, "updated_at")

    def test_review_text_missing(self, valid_place, valid_user):
        """
        Tests that text (comment) is required.
        
        According to the documentation, the text of a review is required.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text=None, rating=5, place=valid_place, user=valid_user)
        assert exception.type == ValueError
        assert "Review text is required" in str(exception.value)

    def test_review_text_empty(self, valid_place, valid_user):
        """
        Tests that text (comment) cannot be empty.
        
        An empty string should be treated the same as None - invalid.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="", rating=5, place=valid_place, user=valid_user)
        assert exception.type == ValueError
        assert "Review text is required" in str(exception.value)

    def test_review_rating_missing(self, valid_place, valid_user):
        """
        Tests that rating is required.
        
        According to the documentation, the rating is required.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=None, place=valid_place, user=valid_user)
        assert exception.type == ValueError
        assert "Rating must be" in str(exception.value)

    def test_review_rating_too_low(self, valid_place, valid_user):
        """
        Tests that rating cannot be less than 1.
        
        According to the documentation, the rating must be between 1 and 5.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=0, place=valid_place, user=valid_user)
        assert exception.type == ValueError
        assert "Rating must be between 1 and 5" in str(exception.value)

    def test_review_rating_too_high(self, valid_place, valid_user):
        """
        Tests that rating cannot be greater than 5.
        
        According to the documentation, the rating must be between 1 and 5.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=6, place=valid_place, user=valid_user)
        assert exception.type == ValueError
        assert "Rating must be between 1 and 5" in str(exception.value)

    def test_review_place_missing(self, valid_user):
        """
        Tests that place is required.
        
        According to the documentation, the place being reviewed is required.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=5, place=None, user=valid_user)
        assert exception.type == ValueError
        assert "Place is required" in str(exception.value)

    def test_review_user_missing(self, valid_place):
        """
        Tests that user (reviewer) is required.
        
        According to the documentation, the user who wrote the review is required.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=5, place=valid_place, user=None)
        assert exception.type == ValueError
        assert "User is required" in str(exception.value)

    def test_review_place_type(self, valid_user):
        """
        Tests that place must be a Place instance.
        
        This ensures type validation for the place attribute.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=5, place="not a place", user=valid_user)
        assert exception.type in [ValueError, TypeError]
        assert "Place must be" in str(exception.value)

    def test_review_user_type(self, valid_place):
        """
        Tests that user must be a User instance.
        
        This ensures type validation for the user attribute.
        """
        with pytest.raises(Exception) as exception:
            review = Review(text="Great place!", rating=5, place=valid_place, user="not a user")
        assert exception.type in [ValueError, TypeError]
        assert "User must be" in str(exception.value)

    def test_review_update(self, valid_review):
        """
        Tests updating review attributes using the update method.
        
        This verifies that:
        1. The update method works as expected
        2. Attributes can be updated
        3. The updated_at timestamp changes
        
        This matches the 'update() method' requirement in the class diagram.
        """
        review = valid_review
        original_updated_at = review.updated_at

        # Update the review
        review.update({
            "text": "Updated review: Still a great place!",
            "rating": 4
        })

        # Check that attributes were updated
        assert review.text == "Updated review: Still a great place!"
        assert review.rating == 4
        assert review.updated_at > original_updated_at

    def test_review_update_invalid(self, valid_review):
        """
        Tests that update method still validates the data.
        
        This ensures that invalid updates are rejected.
        """
        review = valid_review

        # Try to update with invalid rating
        with pytest.raises(Exception) as exception:
            review.update({"rating": 10})
        assert "Rating must be between 1 and 5" in str(exception.value)

        # Verify the original rating is unchanged
        assert review.rating == 5

    def test_review_to_dict(self, valid_review, valid_place, valid_user):
        """
        Tests conversion to dictionary for API responses.
        
        This is important for data serialization needed for the API layer.
        It also verifies that relationship data is properly included.
        """
        review = valid_review
        review_dict = review.to_dict()

        # Check that dictionary contains required fields
        assert review_dict["id"] == review.id
        assert review_dict["text"] == "Great place, highly recommended!"
        assert review_dict["rating"] == 5
        assert review_dict["place_id"] == valid_place.id
        assert review_dict["user_id"] == valid_user.id
        assert "created_at" in review_dict
        assert "updated_at" in review_dict

        # Check that user information is included
        assert "user_info" in review_dict
        assert review_dict["user_info"]["first_name"] == valid_user.first_name
        assert review_dict["user_info"]["last_name"] == valid_user.last_name

    def test_review_create(self, valid_review, valid_place):
        """
        Tests the create() method.
        
        According to the class diagram, Review should have a create() method.
        This should add the review to the place's reviews list and save it.
        """
        review = valid_review

        # Clear the place's reviews list first
        valid_place.reviews = []

        # Call the create method
        result = review.create()

        # Check that create returns the review instance
        assert result == review

        # Check that the review was added to the place's reviews list
        assert review in valid_place.reviews

    def test_review_delete(self, valid_review):
        """
        Tests the delete() method.
        
        According to the class diagram, Review should have a delete() method.
        """
        review = valid_review
        result = review.delete()

        # delete() should return True for success
        assert result is True

    def test_review_list_by_place(self, valid_place, valid_user):
        """
        Tests the list_by_place() class method.
        
        According to the class diagram, Review should have a list_by_place() method
        that returns all reviews for a specific place.
        """
        # Create multiple reviews for the same place
        review1 = Review(text="Great place!", rating=5, place=valid_place, user=valid_user)
        review1.create()

        # Create another user for a different review
        other_user = User("Jane", "Doe", "jane@doe.com", "password456")
        review2 = Review(text="Lovely stay", rating=4, place=valid_place, user=other_user)
        review2.create()

        # Call the list_by_place method
        place_reviews = Review.list_by_place(valid_place)

        # Verify that all reviews for the place are returned
        assert len(place_reviews) >= 0
        review_texts = [r.text for r in place_reviews]
        assert "Great place!" in review_texts
        assert "Lovely stay" in review_texts
