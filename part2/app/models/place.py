from app.models.baseModel import BaseModel
from datetime import datetime


class Place(BaseModel):
    """
    Place class representing accommodation listings in the HBnB application.
    
    Attributes:
        title (str): Title of the place, max 100 characters
        description (str): Detailed description of the place
        price (float): Price per night, must be positive
        latitude (float): Latitude coordinate, between -90.0 and 90.0
        longitude (float): Longitude coordinate, between -180.0 and 180.0
        owner (User): User instance who owns the place
        amenities (list): List of Amenity instances available at the place
        reviews (list): List of Review instances for the place
    """

    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): Title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): User instance who owns the place
            
        Raises:
            ValueError: If validation fails for any field
            TypeError: If owner is not a User instance
        """
        super().__init__()  # Initialize BaseEntity attributes

        # Validate and set attributes
        self.title=title
        self.description= description
        self.price= price
        self.latitude= latitude
        self.longitude= longitude
        self.owner_id= owner_id

        # Initialize lists for relationships
        self.amenities = amenities
        self.reviews = []

    """Title Setter and Getter"""
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        if value is None:
            raise ValueError("Place title is required")
        elif not self.valid_string_length(value, 100):
            raise ValueError("Place title must be less than 100 characters")
        else:
            self.__title = value
    
    """Description Setter and Getter"""
    """Optional parameter"""
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, value):
        self.__description = value if value else ""

    
    """Price Setter and Getter"""
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value is None:
            raise ValueError("Price is required")
        elif value < 0:
            raise ValueError("Price must be a positive value")
        self.__price = float(value)

    """Latitud and longitude Setter and Getter"""
    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """
        Set and validate the latitude.
        
        Args:
            latitude (float): Latitude coordinate
            
        Raises:
            ValueError: If latitude is invalid
        """
        if value is None:
            raise ValueError("Latitude is required")
        elif not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be within the range of -90.0 to 90.0")
        self.__latitude = float(value)

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """
        Set and validate the longitude.
        
        Args:
            longitude (float): Longitude coordinate
            
        Raises:
            ValueError: If longitude is invalid
        """
        if value is None:
            raise ValueError("Longitude is required")
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be within the range of -180.0 to 180.0")
        self.__longitude = float(value)

    """Owner_id Setter and Getter / condition that owner exist"""
       
    @property
    def owner_id(self):
        return self.__owner_id
    
    @owner_id.setter
    def owner_id(self, value):
        """
        Set and validate the owner.
        
        Args:
            owner (User): User instance who owns the place
            
        Raises:
            TypeError: If owner is not a User instance
            ValueError: If owner is not valid
        """
        if value is None:
            raise ValueError("An owner ID is required")
        
        # owner = self.user_repo.get(value)
        
        # if not owner:
        #     raise ValueError("User does not exist")
        self.__owner_id = value

    """Amenities Setter and Getter / optional amenities"""

    @property
    def amenities(self):
        return self.__amenities

    @amenities.setter
    def amenities(self, value):
        self.__amenities = value if value else []

    """Double check what else should be taken into account
    Additional Validation on amenities and reviews"""

    def add_review(self, review):
        if review is None:
            raise ValueError("Review cannot be None")
        self.reviews.append(review)
        self.save()  # Update the updated_at timestamp
        return self

    def add_amenities(self, amenity):
        """
        Add an amenity to the place.

        Args:
            amenity: Amenity instance to add

        Returns:
            Place: The updated place instance with the new amenity
        """
        if amenity is None:
            raise ValueError("Amenity cannot be None")
        self.amenities.append(amenity)
        self.save()  # Update the updated_at timestamp
        return self

    def valid_string_length(self, string, length):
        return len(string) <= length
    
    def serialization(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else None,
            "updated_at": self.updated_at.isoformat() if isinstance(self.created_at, datetime) else None,
            "title": self.title,
            "description" : self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [amenity.serialization() for amenity in self.amenities],
            "reviews": [review.serialization() for review in self.reviews]
        }
