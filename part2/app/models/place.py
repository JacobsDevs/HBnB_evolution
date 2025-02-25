from app.models.baseModel import BaseModel
from app.services.facade import HBnBFacade


data_base = HBnBFacade()

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner_id, amenities=[], description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
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
        elif self.valid_string_length(value, 100) is False:
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
        if value is None:
            pass
        else:
            self.__description = value
    
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

    """Latitud and longitud Setter and Getter"""
    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if value is None:
            raise ValueError("Latitude is required")
        elif not -90 < value < 90:
            raise ValueError("Latitude must be within the range of -90.0 to 90.0")
        self.__latitude = float(value)

    @property
    def longitud(self):
        return self.__longitud

    @longitud.setter
    def longitud(self, value):
        if value is None:
            raise ValueError("Longitud is required")
        if not -180 < value < 180:
            raise ValueError("Longitud must be within the range of -180.0 to 180.0")
        self.__longitud = float(value)

    """Owner_id Setter and Getter / condition that owner exist"""
       
    @property
    def owner_id(self):
        return self.__owner_id
    
    @owner_id.setter
    def owner_id(self, value):
        owner = data_base.user_repo.get(value)
        if value is None:
            raise ValueError("An owner ID is required")
        elif not owner:
            raise ValueError("User does not exist")
        self.__owner_id = value

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def valid_string_length(self, string, length):
        return len(string) <= length
