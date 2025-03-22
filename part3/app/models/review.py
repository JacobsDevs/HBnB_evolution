from part3.app.models.baseModel import BaseModel
from part3.app.models.user import User
from part3.app.extensions import db


class Review(BaseModel):
    """
    Review class representing user reviews for places in the HBnB application.
    
    Attributes:
        text (str): Content of the review
        rating (int): Rating given to the place (1-5)
        place (Place): Place being reviewed
        user (User): User who wrote the review
    """

    __tablename__ = "reviews"

    text = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.Integer, nullable = False)

    # Relationship for Authorization (Foreign Keys)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id=None, user_id=None, place=None, user=None):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): Content of the review
            rating (int): Rating (1-5)
            place_id (str, optional): ID of the place being reviewed
            user_id (str, optional): ID of the user who wrote the review
            place (Place, optional): Place being reviewed
            user (User, optional): User who wrote the review
        """
        super().__init__()  # Initialize BaseEntity attributes

        # Validate and set attributes
        self.set_text(text)
        self.set_rating(rating)

        # Just store the IDs directly, don't fetch the objects
        if place_id:
            self.place_id = place_id
        elif place:
            self.place = place
            
        if user_id:
            self.user_id = user_id
        elif user:
            self.user = user

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
        from part3.app.models.place import Place
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
    
    def serialize(self):
        """
        Convert the review to a dictionary for API responses.
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': str(self.created_at),  # Convert to string
            'updated_at': str(self.updated_at)   # Convert to string
        }
