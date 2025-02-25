from app.models.baseModel import BaseModel


class Amenity(BaseModel):
    """
    Amenity class representing features or services available at a place.
    
    Attributes:
        name (str): Name of the amenity (e.g., "Wi-Fi", "Parking")
        description (str): Detailed description of the amenity
    """

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

    def create(self):
        """
        Create a new amenity.
        
        Returns:
            Amenity: The created amenity instance
        """
        self.save()
        return self

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

    def delete(self):
        """
        Delete the amenity from memory(RAM).
        
        Returns:
            bool: True if deletion was successful
        """
        # In real implementation, this would interact with the repository
        return True

    @classmethod
    def list_all(cls):
        """
        List all amenities.
        In a real application, this would query the repository.
        
        Returns:
            list: List of all Amenity instances
        """
        # In real implementation, this would interact with the repository
        # return repository.get_all()
        return []

    def to_dict(self):
        """
        Convert the amenity to a dictionary.
        
        Returns:
            dict: Dictionary containing amenity attributes
        """
        return super().to_dict()
