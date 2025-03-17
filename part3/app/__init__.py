from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, bcrypt, jwt
from app.config import config

def create_app(config_name="development"):
    app = Flask(__name__)

    # Apply configuration to the app
    app.config.from_object(config[config_name])

    # Config JWT Specific Settings
    app.config["JWT_SECRET_KEY"] = app.config.get("SECRET_KEY", "default-jwt-key")
    # default-jwt-key is the "fall back key if no SECRET KEY is present"


    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    # Import namespaces after app is created to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns

    api = Api(app, version=1.0, title='HBnB API', description='HBnb Application API')

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
