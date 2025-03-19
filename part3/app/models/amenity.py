from app.models.baseModel import BaseModel
from app import db


class Amenity(BaseModel):
    """
    Amenity class representing features or services available at a place.
    
    Attributes:
        name (str): Name of the amenity (e.g., "Wi-Fi", "Parking")
        description (str): Detailed description of the amenity
    """

    __tablename__ = "amenities"

    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(50), nullable = False) 
    description = db.Column(db.String(128)) 



    def __init__(self, name, description=None):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): Name of the amenity
            description (str, optional): Description of the amenity
            
        Raises:
            ValueError: If validation fails for the name
        """
        super().__init__()  # Initialize BaseEntity attributes

        # Validate and set attributes
        self.set_name(name)
        self.description = description  # Description is optional

    def set_name(self, name):
        """
        Set and validate the amenity name.
        
        Args:
            name (str): Name of the amenity
            
        Raises:
            ValueError: If name is invalid
        """
        if not name:
            raise ValueError("Amenity name is required")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        self.name = name

    def update(self, data):
        """
        Update the amenity information.
        
        Args:
            data (dict): Dictionary containing new attribute values
            
        Returns:
            Amenity: The updated amenity instance
        """
        # Special handling for validated fields
        if 'name' in data:
            self.set_name(data.pop('name'))

        # Update remaining fields using the base method
        super().update(data)
        return self
