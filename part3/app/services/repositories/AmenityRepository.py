from part3.app.models.amenity import Amenity
from part3.app import db
from part3.app.persistence.SQLAlchemy_repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        return self.model.query.filter_by(name=name).first()

    def get_amenity_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
