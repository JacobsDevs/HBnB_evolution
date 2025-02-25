from app.models.baseModel import BaseModel
from app.models.user import User

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

    def __init__(self, title, description, price, latitude, longitude, owner):
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
        self.set_title(title)
        self.set_description(description)
        self.set_price(price)
        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_owner(owner)

        # Initialize lists for relationships
        self.amenities = []
        self.reviews = []

    def set_title(self, title):
        """
        Set and validate the title.
        
        Args:
            title (str): Title of the place
            
        Raises:
            ValueError: If title is invalid
        """
        if not title:
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self.title = title

    def set_description(self, description):
        """
        Set the description (optional).
        
        Args:
            description (str): Description of the place
        """
        self.description = description  # Description is optional

    def set_price(self, price):
        """
        Set and validate the price.
        
        Args:
            price (float): Price per night
            
        Raises:
            ValueError: If price is invalid
        """
        try:
            price_value = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a number")

        if price_value <= 0:
            raise ValueError("Price must be positive")

        self.price = price_value

    def set_latitude(self, latitude):
        """
        Set and validate the latitude.
        
        Args:
            latitude (float): Latitude coordinate
            
        Raises:
            ValueError: If latitude is invalid
        """
        try:
            lat_value = float(latitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number")

        if lat_value < -90.0 or lat_value > 90.0:
            raise ValueError("Latitude must be between -90 and 90")

        self.latitude = lat_value

    def set_longitude(self, longitude):
        """
        Set and validate the longitude.
        
        Args:
            longitude (float): Longitude coordinate
            
        Raises:
            ValueError: If longitude is invalid
        """
        try:
            long_value = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number")

        if long_value < -180.0 or long_value > 180.0:
            raise ValueError("Longitude must be between -180 and 180")

        self.longitude = long_value

    def set_owner(self, owner):
        """
        Set and validate the owner.
        
        Args:
            owner (User): User instance who owns the place
            
        Raises:
            TypeError: If owner is not a User instance
            ValueError: If owner is not valid
        """
        if not owner:
            raise ValueError("Owner is required")
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")

        self.owner = owner

    def create(self):
        """
        Create a new place.
        
        Returns:
            Place: The created place instance
        """
        self.save()
        return self

    def update(self, data):
        """
        Update the place information.
        
        Args:
            data (dict): Dictionary containing new attribute values
            
        Returns:
            Place: The updated place instance
        """
        # Special handling for validated fields
        if 'title' in data:
            self.set_title(data.pop('title'))

        if 'description' in data:
            self.set_description(data.pop('description'))

        if 'price' in data:
            self.set_price(data.pop('price'))

        if 'latitude' in data:
            self.set_latitude(data.pop('latitude'))

        if 'longitude' in data:
            self.set_longitude(data.pop('longitude'))

        if 'owner' in data:
            self.set_owner(data.pop('owner'))

        # Update remaining fields using the base method
        super().update(data)
        return self

    def delete(self):
        """
        Delete the place.
        
        Returns:
            bool: True if deletion was successful
        """
        # In real implementation, this would interact with the repository
        return True

    def add_review(self, review):
        """
        Add a review to the place.
        
        Args:
            review: Review instance to add
            
        Returns:
            Place: The updated place instance with the new review
        """
        # Ensure the review is for this place
        if review.place.id != self.id:
            raise ValueError("Review must be for this place")

        self.reviews.append(review)
        self.save()  # Update the updated_at timestamp
        return self

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.
        
        Args:
            amenity: Amenity instance to add
            
        Returns:
            Place: The updated place instance with the new amenity
        """
        # Check if amenity already exists for this place
        if any(a.id == amenity.id for a in self.amenities):
            return self  # Amenity already exists, no need to add

        self.amenities.append(amenity)
        self.save()  # Update the updated_at timestamp
        return self

    def remove_amenity(self, amenity_id):
        """
        Remove an amenity from the place.
        
        Args:
            amenity_id: ID of the amenity to remove
            
        Returns:
            Place: The updated place instance
        """
        self.amenities = [a for a in self.amenities if a.id != amenity_id]
        self.save()  # Update the updated_at timestamp
        return self

    @classmethod
    def list_by_owner(cls, owner):
        """
        List all places owned by a specific user.
        In a real application, this would query the repository.
        
        Args:
            owner (User): User instance to filter by
            
        Returns:
            list: List of Place instances owned by the user
        """
        # In real implementation, this would interact with the repository
        # return repository.get_all_by_attribute('owner_id', owner.id)
        return []

    def to_dict(self):
        """
        Convert the place to a dictionary.
        
        Returns:
            dict: Dictionary containing place attributes
        """
        place_dict = super().to_dict()

        # Handle relationships
        if hasattr(self, 'owner'):
            place_dict['owner_id'] = self.owner.id
            # Include additional owner information
            place_dict['owner_info'] = {
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }

        # Format amenities as a list of IDs
        if hasattr(self, 'amenities') and self.amenities:
            place_dict['amenity_ids'] = [amenity.id for amenity in self.amenities]

        # Format reviews as a list of IDs
        if hasattr(self, 'reviews') and self.reviews:
            place_dict['review_ids'] = [review.id for review in self.reviews]

        return place_dict
