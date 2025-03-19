from app.models.place import Place
from app import db
from app.persistence.SQLAlchemy_repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_place_by_title(self, title):
        return self.model.query.filter_by(title=title).first()

    def get_place_by_id(self, id):
        return self.model.query.filter_by(id=id).first()

    def get_place_by_location(self, latitude, longitude):
        return self.model.query.filter_by(latittude = latitude, longitude=longitude).first()
    
    # Maybe implement get places by PriceRange ?
    # Should ther be a method get ammenities from place ID ?

    # Check how can we get te next two methods on ReviewRepository

    # def get_reviews_by_placeID(self, place_id):
    #     return self.model.query.filter_by(id=place_id).all()
    
    # def get_reviews_by_userID(self, user_id):
    #     return self.model.query.filter_by(id=user_id).all()

