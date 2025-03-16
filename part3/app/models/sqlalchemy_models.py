from app.extensions import db
from sqlalchemy.sql import func
import uuid

# Association table for many-to-many relationship between places and amenities
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id')),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'))
)

class User(db.Model):