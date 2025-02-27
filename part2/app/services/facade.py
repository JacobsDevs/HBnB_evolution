from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import json

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
        from app.models.user import User

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

#     def get_place(self, place_id):
#         pass

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
