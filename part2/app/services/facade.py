from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """
    The HBnBFacade class acts as a bridge between the API layer and the model/persistence layers.
    
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
    
   
    # Place Operations

    def create_place(self, place_data):
        """Create a Place Object"""
       
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            amenities=place_data.get('amenities'),
            owner_id=place_data.get('owner_id'),
            # user_repo=place_data.get('user_repo')
        )

        self.place_repo.add(place)
        return place
        
    
    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        return place.serialization()
    
    def get_all_places(self):
        all_places = self.place_repo.get_all()
        json_places = [item.serialization() for item in all_places]
        return json_places
        
    def update_place(self, place_id, place_data):
        new_data = self.place_repo.update(place_id, place_data)
        return new_data.serialization()





#     def get_place(self, place_id):
#         pass

# # === Amenity ===

# def create_amenity(self, amenity_data):
#     """
#     Create a new amenity and store it in the repository.
    
#     Args:
#         amenity_data (dict): Dictionary containing amenity data
#             - name (str): Name of the amenity (required)
#             - description (str, optional): Description of the amenity
            
#     Returns:
#         Amenity: The created amenity instance
            
#     Raises:
#         ValueError: If validation fails (e.g., missing name, name too long)
#     """
#     # Import here to avoid circular imports
#     from app.models.amenity import Amenity

#     # Create a new amenity instance
#     amenity = Amenity(
#         name=amenity_data.get('name'),
#         description=amenity_data.get('description')
#     )

#     # Store in repository
#     self.amenity_repo.add(amenity)

#     return amenity

# def get_amenity(self, amenity_id):
#     """
#     Retrieve an amenity by ID.
    
#     Args:
#         amenity_id (str): ID of the amenity to retrieve
        
#     Returns:
#         Amenity: The amenity instance if found, None otherwise
#     """
#     return self.amenity_repo.get(amenity_id)

# def get_all_amenities(self):
#     """
#     Retrieve all amenities.
    
#     Returns:
#         list: List of all Amenity instances
#     """
#     return self.amenity_repo.get_all()

# def update_amenity(self, amenity_id, amenity_data):
#     """
#     Update an amenity's information.
    
#     Args:
#         amenity_id (str): ID of the amenity to update
#         amenity_data (dict): Dictionary containing updated amenity data
#             - name (str, optional): New name for the amenity
#             - description (str, optional): New description for the amenity
            
#     Returns:
#         Amenity: The updated amenity instance
            
#     Raises:
#         ValueError: If amenity not found or validation fails
#     """
#     # Get the amenity from the repository
#     amenity = self.amenity_repo.get(amenity_id)
#     if not amenity:
#         raise ValueError(f"Amenity with ID {amenity_id} not found")

#     # Update the amenity with the new data
#     amenity.update(amenity_data)

#     return amenity
