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
            if not 1 <= rating_value <= 5:
                raise ValueError("Rating must be between 1 and 5")
            self.rating = rating_value
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer")

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
