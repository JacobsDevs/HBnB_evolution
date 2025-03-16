from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions instances to prevent "circular dependencies"
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
