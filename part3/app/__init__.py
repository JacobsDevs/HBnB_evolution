from flask import Flask
from flask_restx import Api
from datetime import datetime
from app.extensions import bcrypt, jwt

from app.services.facade import facade
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns

def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)

    # Apply configuration to the app
    app.config.from_object(config_class)

    # Initialize Bcrypt with the app
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Config JWT Specific Settings
    app.config["JWT_SECRET_KEY"] = app.config.get("SECRET_KEY", "default-jwt-key")

    api = Api(app, version=1.0, title='HBnB aPI', description='HBnb Application API')

    #register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
