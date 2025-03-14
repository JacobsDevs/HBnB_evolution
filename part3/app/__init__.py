from flask import Flask
from flask_restx import Api
from datetime import datetime
from flask_bcrypt import Bcrypt
from app.services.facade import facade
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns

# Create Bcrypt instance
bcrypt = Bcrypt()

def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)

    # Apply configuration to the app
    app.config.from_object(config_class)

    # Initialize Bcrypt with the app
    bcrypt.init_app(app)

    api = Api(app, version=1.0, title='HBnB aPI', description='HBnb Application API')

    #register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
