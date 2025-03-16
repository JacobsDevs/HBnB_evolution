from app.persistence.repository import Repository
from app.extensions import db
from app.models.sqlalchemy_models import User, Place, Amenity, Review
from sqlalchemy.exc import SQLAlchemyError
import logging # This is if we want to log the errors to the DB or we can just use ValueError instead

class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy implementation of the Repository interface.
    
    This repository uses SQLAlchemy ORM to interact with a relational database,
    replacing the in-memory storage with persistent database storage.
    """
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id): 
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.mdoel, attr_name) == attr_value).first()
