from part3.app.models.review import Review
from part3.app import db
from part3.app.persistence.SQLAlchemy_repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_review_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
    
    def get_review_by_rating(self, rating):
        return self.model.query.filter_by(rating=rating).all()

    # def get_reviews_by_placeID(self, place_id):
    #     return self.model.query.filter_by(id=place_id).all()
    
    # def get_reviews_by_userID(self, user_id):
    #     return self.model.query.filter_by(id=user_id).all()
