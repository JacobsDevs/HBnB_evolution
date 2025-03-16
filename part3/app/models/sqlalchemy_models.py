from app.extensions import db
from sqlalchemy.sql import func
import uuid

# Association table for many-to-many relationship between places and amenities
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id')),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'))
)


# This section is where we are basically creating the table layouts for the DB server once it's connected (ORM method)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

class Place(db.Model):

class Amenity(db.Model):

class Review(db.Model):

