from app.models.baseModel import BaseModel
from app.models.user import User


class Review(BaseModel):
    """
    Review class representing user reviews for places in the HBnB application.
    
    Attributes:
        text (str): Content of the review
        rating (int): Rating given to the place (1-5)
        place (Place): Place being reviewed
        user (User): User who wrote the review
    """

    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): Content of the review
            rating (int): Rating (1-5)
            place (Place): Place being reviewed
            user (User): User who wrote the review
            
        Raises:
            ValueError: If validation fails for any field
            TypeError: If place or user are not correct instance types
        """
        super().__init__()  # Initialize BaseEntity attributes
        
        # Validate and set attributes
        self.set_text(text)
        self.set_rating(rating)
        self.set_place(place)
        self.set_user(user)

    def set_text(self, text):
        """
        Set and validate the review text.
        
        Args:
            text (str): Content of the review
            
        Raises:
            ValueError: If text is invalid
        """
        if not text:
            raise ValueError("Review text is required")
        self.text = text

    def set_rating(self, rating):
        """
        Set and validate the rating.
        
        Args:
            rating (int): Rating (1-5)
            
        Raises:
            ValueError: If rating is invalid
        """
        try:
            rating_value = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer")
            
        if rating_value < 1 or rating_value > 5:
            raise ValueError("Rating must be between 1 and 5")
            
        self.rating = rating_value

    def set_place(self, place):
        """
        Set and validate the place.
        
        Args:
            place (Place): Place being reviewed
            
        Raises:
            TypeError: If place is not a Place instance
            ValueError: If place is not valid
        """
        if not place:
            raise ValueError("Place is required")
            
        # Import Place here to avoid circular imports
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("Place must be a Place instance")
            
        self.place = place

    def set_user(self, user):
        """
        Set and validate the user.
        
        Args:
            user (User): User who wrote the review
            
        Raises:
            TypeError: If user is not a User instance
            ValueError: If user is not valid
        """
        if not user:
            raise ValueError("User is required")
        if not isinstance(user, User):
            raise TypeError("User must be a User instance")
            
        self.user = user

    def create(self):
        """
        Create a new review.
        Also adds the review to the place's review list.
        
        Returns:
            Review: The created review instance
        """
        # Add this review to the place's review list
        if hasattr(self, 'place') and self.place:
            self.place.add_review(self)
            
        self.save()
        return self

    def update(self, data):
        """
        Update the review information.
        
        Args:
            data (dict): Dictionary containing new attribute values
            
        Returns:
            Review: The updated review instance
        """
        # Special handling for validated fields
        if 'text' in data:
            self.set_text(data.pop('text'))
            
        if 'rating' in data:
            self.set_rating(data.pop('rating'))
            
        # Update remaining fields using the base method
        super().update(data)
        return self

    def delete(self):
        """
        Delete the review.
        
        Returns:
            bool: True if deletion was successful
        """
        # In real implementation, this would interact with the repository
        return True

    @classmethod
    def list_by_place(cls, place):
        """
        List all reviews for a specific place.
        In a real application, this would query the repository.
        
        Args:
            place: Place instance to filter by
            
        Returns:
            list: List of Review instances for the place
        """
        # In real implementation, this would interact with the repository
        # return repository.get_all_by_attribute('place_id', place.id)
        return []
    def to_dict(self):
        """
        Convert the review to a dictionary.
        
        Returns:
            dict: Dictionary containing review attributes
        """
        review_dict = super().to_dict()
        
        # Add reference IDs
        if hasattr(self, 'place'):
            review_dict['place_id'] = self.place.id
            
        if hasattr(self, 'user'):
            review_dict['user_id'] = self.user.id
            # Include additional user information
            review_dict['user_info'] = {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
            
        return review_dict
