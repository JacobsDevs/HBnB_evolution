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
    def __init__(self, model_class):
        self.model = model_class

    def add(self, obj):
        """
        Add an object to the DB
        Could be any class of object (User, Place, Amenity, Review)
        """
        try:
            # Create a new instance of the model class with data from the object
            if self.model_class == User:
                db_obj = User(
                    id=obj.id,
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    email=obj.email,
                    password=obj.password,
                    is_admin=obj.is_admin,
                    created_at=obj.created_at,
                    updated_at=obj.updated_at
                )
            elif self.model_class == Place:
                db_obj = Place(
                    id=obj.id,
                    title=obj.title,
                    description=obj.description,
                    price=obj.price,
                    latitude=obj.latitude,
                    longitude=obj.longitude,
                    owner_id=obj.owner_id,
                    created_at=obj.created_at,
                    updated_at=obj.updated_at
                )
                # Add amenities if they exist
                if hasattr(obj, 'amenities') and obj.amenities:
                    for amenity_id in obj.amenities:
                        amenity = db.session.query(Amenity).get(amenity_id)
                        if amenity:
                            db_obj.amenities.append(amenity)
            elif self.model_class == Amenity:
                db_obj = Amenity(
                    id=obj.id,
                    name=obj.name,
                    description=obj.description,
                    created_at=obj.created_at,
                    updated_at=obj.updated_at
                )
            elif self.model_class == Review:
                db_obj = Review(
                    id=obj.id,
                    text=obj.text,
                    rating=obj.rating,
                    place_id=obj.place_id,
                    user_id=obj.user_id,
                    created_at=obj.created_at,
                    updated_at=obj.updated_at
                )
            else:
                raise ValueError(f"Unsupported model class: {self.model_class}")
                
            db.session.add(db_obj)
            db.session.commit()
            
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Database error during add: {str(e)}")
            raise

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
