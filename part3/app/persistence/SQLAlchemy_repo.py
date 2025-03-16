from app.extensions import db # extensions.py is the central instance location
from app.models import User, Place, Review, Amenity
from app.persistence.repository import Repository

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add new object to the database"""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise ValueError (f"Error adding object: {str(e)}")

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                db.session.commit()
                return obj
            except Exception as e:
                db.session.rollback()
                raise ValueError(f"Error updating object: {str(e)}")
        return None

    def delete(self, obj_id): 
        obj = self.get(obj_id)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                raise ValueError(f"Error deleting object: {str(e)}")
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

