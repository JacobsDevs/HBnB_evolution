from ..persistence.repository import InMemoryRepository
from ..models.place import Place
from ..models.review import Review
from ..models.amenity import Amenity
from ..models.user import User
import json

class HBnBFacade:
    """
    The HBnBFacade class acts as a bridge between the API layer and the model/persistence layers.

    <==|==> CRUD operations should be handled here in the facade <==|==>
    
    This class follows the Facade design pattern, which provides a simplified interface
    to a complex subsystem. It coordinates all operations involving models and repositories,
    centralizing business logic and keeping the API layer clean.
    """

    def __init__(self):
        """
        Initialize repositories for each entity type.
        Each repository is responsible for storing and retrieving a specific entity type.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User operations
    def create_user(self, user_data):

        """
        Create a new user and store it in the repository.
        
        Args:
            user_data (dict): Dictionary containing user data
            
        Returns:
            User: The created user instance
            
        Raises:
            ValueError: If validation fails
        """
        # Create a new user instance with the provided data
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password'),
            is_admin=user_data.get('is_admin', False)
        )

        # Store in repository
        self.user_repo.add(user)

        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        users = self.user_repo.get_all()
        return [c.__dict__ for c in users]

    # === Place === (TEMP)

    def get_place(self, place_id):
        """
        Retrieve a place by its ID.

        Args:
            place_id (str): ID of the place to retrieve
        Returns:
            Place: The place instance if found, None otherwise
        """
        return self.place_repo.get(place_id)

# === Amenity ===

    def create_amenity(self, amenity_data):
        """
        Create a new amenity and store it in the repository.
        Args:
            amenity_data (dict): Dictionary containing amenity data
            - name (str): Name of the amenity (required)
            - description (str, optional): Description of the amenity
        Returns:
            Amenity: The created amenity instance
        Raises:
            ValueError: If validation fails (e.g., missing name, name too long)
        """
        # Create a new amenity instance
        amenity = Amenity(
            name=amenity_data.get('name'),
            description=amenity_data.get('description')
        )

        # Store in repository
        self.amenity_repo.add(amenity)

        return amenity

    def delete_amenity(self, amenity_id):
        """
        Delete an amenity.
        Args:
            amenity_id (str): ID of the amenity to delete
        Returns:
            bool: True if deletion was successful, False if amenity not found
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False

        self.amenity_repo.delete(amenity_id)
        return True

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity ID. 

        Args:
            amenity_id (str): ID of the amenity to retrieve
        Returns:
            Amenity: The amenity instance(object) if found, None otherwise
        """

        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.
        Returns:
            List: List of all Amenity instances (objects)
        """
        amenities = self.amenity_repo.get_all()
        return [a.__dict__ for a in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity's information
        
        Args:
            amenity_id (str): ID of the amenity to update
            amenity_data (dict): Complete amenity data

        Returns:
            Amenity: The updated amenity instance
        Raises:
            ValueError: if amenity not found or validation fails
        """
        # Get the existing amenity
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        # Update the amenity
        amenity.name = amenity_data.get('name')
        amenity.description = amenity_data.get('description')

        # Save the updated amenity
        self.amenity_repo.update(amenity_id, amenity_data)

        return amenity


# === Review ===
# [x] create_review
# [x]  get_review
# [x]  get_all_reviews
# [x] update_review
# [x]  delete_review

    def create_review(self, review_data):
        """
        Create a new review and store it in the repository.
        """

        # Get place and user objects first
        place = self.get_place(review_data.get('place_id'))
        user = self.get_user(review_data.get('user_id'))

        # Fail safe
        if not place:
            raise ValueError(f"Place with ID {review_data.get('place_id')} not found")

        if not user:
            raise ValueError(f"User with ID {review_data.get('user_id')} not found")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user
        )

        # Store in repository
        self.review_repo.add(review)

        return review

    def delete_review(self, review_id):
        """
        Delete a review.
        Args:
            review_id (str): ID of the review to delete
        Returns:
            bool: True if deletion was successful, False if review not found
        """
        review = self.get_review(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True

    def get_review(self, review_id):
        """
        Retrieve a review ID. 

        Args:
            review_id (str): ID of the review to retrieve
        Returns:
            review: The review instance(object) if found, None otherwise
        """

        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all reviews.

        Returns:
            List: List of all Reviews as dictionaries
        """
        reviews = self.review_repo.get_all()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place.id,
                'user_id': review.user.id,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            } for review in reviews
        ]

    def update_review(self, review_id, review_data):
        """
        Update a review's information (Data)
        """
        # Get the review from the repository
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Update only the provided fields
        if 'text' in review_data:
            review.set_text(review_data['text'])

        if 'rating' in review_data:
            review.set_rating(review_data['rating'])

        # Save the updated review
        self.review_repo.update(review_id, review_data)

        return review


facade = HBnBFacade()
# Create a single application-wide instance of HBnBFacade
# This follows a singleton-like pattern to ensure all modules
# import and use the same facade instance, maintaining consistent
# state across the application and providing centralized access
# to all repositories
