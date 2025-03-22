from part3.app.models.baseModel import BaseModel
from part3.app.extensions import db
from sqlalchemy.orm import validates

# Relationship Association Table (Place > Amenity)
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

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
    __tablename__ = "places"

    # id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)

    # Add relationships back to the above place_amenity outside of the class
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', 
                         backref=db.backref('places', lazy=True))



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

        # Validate and set attributes
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        # Initialize lists for relationships
        self.amenities = amenities
        self.reviews = []
    
    @validates("title")
    def validate_title(self, key, value):
        if value is None:
            raise ValueError("Place title is required")
        elif not self.valid_string_length(value, 100):
            raise ValueError("Place title must be less than 100 characters")
        else:
            return value
    
        
    @validates("description")
    def validate_description(self, key, value):
        description = value if value else ""
        return description

    
    @validates("price")
    def validate_price(self, key, value):
        if value is None:
            raise ValueError("Price is required")
        elif value < 0:
            raise ValueError("Price must be a positive value")
        return float(value)

    @validates("latitude")
    def validate_latitude(self, key, value):
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
        return float(value)

    @validates("longitude")
    def validate_longitude(self, key, value):
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
        return float(value)
           
    @validates("owner_id")
    def validate_owner_id(self, key, value):
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
        return value

    @validates("amenities")
    def validate_amenities(self, key, value):
        amenities = value if value else []
        return amenities

    def add_review(self, review):
        """ Add a review to the place """
        if review is None:
            raise ValueError("Review cannot be None")
    
        # Check if the review is already in the reviews list
        if not hasattr(self, 'reviews'):
            self.reviews = []
    
        if review not in self.reviews:
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
        if amenity is None:
            raise ValueError("Amenity cannot be None")
        
        # Ensure the amenities attribute exists
        if not hasattr(self, 'amenities') or self.amenities is None:
            self.amenities = []
        
        # Check if the amenity is already in the list (prevent duplicates)
        # First try to check by ID
        amenity_ids = [a.id for a in self.amenities if hasattr(a, 'id')]
        if hasattr(amenity, 'id') and amenity.id in amenity_ids:
            # Already have this amenity
            return self
            
        # If we don't have it by ID, add it
        self.amenities.append(amenity)
        self.save()  # Update the updated_at timestamp
        
        return self

    def valid_string_length(self, string, length):
        return len(string) <= length
    
    def serialization(self):
        """
        Convert the place to a dictionary for API responses.
        """
        # Process amenities
        amenities_data = []
        if hasattr(self, 'amenities') and self.amenities:
            for amenity in self.amenities:
                if amenity is not None:
                    amenity_data = {
                        'id': amenity.id,
                        'name': amenity.name
                    }
                    if hasattr(amenity, 'description'):
                        amenity_data['description'] = amenity.description
                    amenities_data.append(amenity_data)
        
        # Process reviews
        reviews_data = []
        if hasattr(self, 'reviews') and self.reviews:
            for review in self.reviews:
                if review is not None:
                    review_data = {
                        'id': review.id,
                        'text': review.text,
                        'rating': review.rating,
                        'created_at': str(review.created_at),
                        'updated_at': str(review.updated_at)
                    }
                    if hasattr(review, 'user') and review.user:
                        review_data['user_id'] = review.user.id
                    reviews_data.append(review_data)
        
        return {
            "id": self.id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": amenities_data,
            "reviews": reviews_data
        }
