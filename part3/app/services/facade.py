from app.services.repositories.UserRepository import UserRepository
from app.services.repositories.PlaceRepository import PlaceRepository
from app.services.repositories.ReviewRepository import ReviewRepository
from app.services.repositories.AmenityRepository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

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
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

# === User operations ===
    def create_user(self, user_data):
        """
        Create a new user and store it in the repository.
        """
        # Create the User
        user = User(**user_data)
        # Store the User
        self.user_repo.add(user)
        # Return the User
        return user.serialized

    def get_user(self, user_id):
        print(f"Looking for user with ID: {user_id}")
        all_users = self.user_repo.get_all()
        print(f"Available users: {[u.id for u in all_users]}")
        
        user = self.user_repo.get(user_id)
        print(f"Found user: {user}")
        
        return user

    def get_user_by_parameter(self, key, value):
        return self.user_repo.get_by_attribute(key, value)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        users = self.user_repo.get_all()
        print(f"All users in repository: {[u.id for u in users]}")
        return [u.serialize() for u in users]

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user == None:
            return None
        # Check all available fields when updating
        if any(x not in ['first_name', 'last_name', 'email', 'password', 'is_admin'] for x in user_data.keys()):
            return False
        # process password separate due to hashing requirement
        if 'password' in user_data:
            password = user_data.pop('password')
            user.hash_password(password)

        user.update(user_data)
        return user

    def delete_user(self, user_id):
        """
        Delete a user by ID

        Args: user_id (str): ID of the user to delete

        Returns:
            bool: True if user was deleted, False if user not found
        """

        user = self.user_repo.get(user_id)
        if not user:
            return False

        self.user_repo.delete(user_id)
        return True
      
# === Place Operations ===

    def create_place(self, place_data):
        """Create a Place Object with optional amenities"""
        
        # Extract amenity IDs from the request
        amenity_ids = place_data.get('amenities', [])
        amenities = []
        
        # Get actual amenity objects from the repository
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)
        
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            amenities=amenities,
            owner_id=place_data.get('owner_id'),
        )

        self.place_repo.add(place)
        return place
        
    def get_place(self, place_id):
        """
        Retrieve a place by its ID.

        Args:
            place_id (str): ID of the place to retrieve
        Returns:
            dict: The place data as a dictionary if found, None otherwise
        """
        place = self.place_repo.get(place_id)
        if place is None:
            return None
            
        # Return the serialized place, not the place object itself
        return place.serialization()

    def get_all_places(self):
        all_places = self.place_repo.get_all()
        json_places = [item.serialization() for item in all_places]
        return json_places
        
    def update_place(self, place_id, place_data):
        new_data = self.place_repo.update(place_id, place_data)
        return new_data.serialization()

    def delete_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return False

        self.place_repo.delete(place_id)
        return True
    
    def get_place_by_title(self, title):
        return self.place_repo.get_place_by_title(title)

    def get_place_by_id(self, id):
        return self.place_repo.get_place_by_id(id)

    def get_place_by_location(self, latitude, longitude):
        return self.place_repo.get_place_by_location(latitude, longitude)
    

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
        Retrieve an amenity by its ID.

        Args:
            amenity_id (str): ID of the amenity to retrieve
        Returns:
            Amenity: The amenity instance if found, None otherwise
        """
        # Debug output
        print(f"Looking for amenity with ID: {amenity_id}")
        all_amenities = self.amenity_repo.get_all()
        print(f"Available amenities: {[a.id for a in all_amenities]}")
        
        # Try to get the amenity
        amenity = self.amenity_repo.get(amenity_id)
        print(f"Found amenity: {amenity}")
        
        return amenity

    def get_all_amenities(self):
        """
        Retrieve all amenities.
        Returns:
            List: List of all Amenity instances as dictionaries
        """
        amenities = self.amenity_repo.get_all()
        return [{
            'id': a.id,
            'name': a.name,
            'description': a.description if hasattr(a, 'description') else "",
            'created_at': a.created_at,
            'updated_at': a.updated_at
        } for a in amenities]

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

    def get_amenities_by_place(self, place_id):
        """
        Retrieve all amenities for a specific place.
        
        Args:
            place_id (str): ID of the place
            
        Returns:
            list: List of amenities for the place, or None if place not found
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
            
        return place.amenities

    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Add an amenity to a place.
        
        Args:
            place_id (str): ID of the place
            amenity_id (str): ID of the amenity
            
        Returns:
            bool: True if successful, False otherwise
        """
        place = self.place_repo.get(place_id)
        if not place:
            return False
            
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
            
        place.add_amenity(amenity)
        return True
            
    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_amenity_by_name(name)

    def get_amenity_by_id(self, id):
        return self.amenity_repo.get_amenity_by_id(id)


# === Review ===

    def create_review(self, review_data):
        """
        Create a new review and store it in the repository.
        Additionally, link the review to its associated place.
        """
        # Get place and user objects first
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')
        
        # Debug all repository data
        print(f"Looking for user with ID: {user_id}")
        all_users = self.user_repo.get_all()
        print(f"All users in repository: {[u.id for u in all_users]}")
        
        # Get the raw objects, not serialized versions
        place_obj = self.place_repo.get(place_id)
        user_obj = self.user_repo.get(user_id)
        
        print(f"Found place: {place_obj}")
        print(f"Found user: {user_obj}")

        # Fail safe
        if not place_obj:
            raise ValueError(f"Place with ID {place_id} not found")

        if not user_obj:
            raise ValueError(f"User with ID {user_id} not found")

        # Create review with direct object references
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place_obj,
            user=user_obj
        )

        # Store in repository
        self.review_repo.add(review)
        
        # Add the review to the place's reviews list
        place_obj.add_review(review)
        
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

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.
        
        Args:
            place_id (str): ID of the place
        
        Returns:
            list: List of reviews for the place
        """
        place = self.get_place(place_id)
        if not place:
            return None

        # Return the reviews from the place object
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            } for review in place.reviews
        ]

    def has_user_reviewed_place(self, user_id, place_id):
        """
        Check if the user has already reviewed a place

        Args:   user_id (str): ID of user
                place_id (str): ID of the place
        
        Returns:
                bool: True if the user has already reviewed the place, False otherwise
        """
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user_id is user_id and review.place_id is place_id:
                return True
            return False
        
    def get_review_by_id(self, id):
        return self.review_repo.get_review_by_id(id)
    
    def get_review_by_rating(self, rating):
        return self.review_repo.get_review_by_rating(rating)


facade = HBnBFacade()
# Create a single application-wide instance of HBnBFacade
# This follows a singleton-like pattern to ensure all modules
# import and use the same facade instance, maintaining consistent
# state across the application and providing centralized access
# to all repositories
