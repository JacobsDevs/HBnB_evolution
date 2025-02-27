import uuid
from datetime import datetime

class BaseModel:
    """
    Base class for all entities in the HBnB application.
    
    Provides common attributes and methods that will be inherited by all entity classes:
    - id: A UUID string that uniquely identifies each entity
    - created_at: Timestamp when the entity is created
    - updated_at: Timestamp when the entity is last updated
    """

    def __init__(self):
        """
        Initialize a new BaseEntity instance with:
        - A unique UUID as a string
        - The current datetime for both created_at and updated_at
        """
        self.id = str(uuid.uuid4())  # Generate a random UUID and convert to string
        self.created_at = str(datetime.now())  # Set creation timestamp
        self.updated_at = str(datetime.now())  # Set initial update timestamp

    def save(self):
        """
        Update the updated_at timestamp whenever the entity is modified.
        This should be called whenever an entity's attributes are changed.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the entity based on the provided dictionary.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Note:
            - Only updates attributes that already exist on the entity
            - Updates the updated_at timestamp
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)

        # Update the timestamp
        self.save()

    def to_dict(self):
        """
        Convert the entity to a dictionary representation.
        Useful for serialization and API responses.
        
        Returns:
            dict: Dictionary containing all entity attributes
        """
        entity_dict = self.__dict__.copy()

        # Convert datetime objects to ISO format strings for better serialization
        entity_dict['created_at'] = self.created_at.isoformat()
        entity_dict['updated_at'] = self.updated_at.isoformat()

        # Add class name for type information
        entity_dict['__class__'] = self.__class__.__name__

        return entity_dict
