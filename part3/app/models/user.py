from app.models.baseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
from app import bcrypt, db
from sqlalchemy.orm import validates

class User(BaseModel):
    """User Model
    Contains all the information for a user.

    Attributes:
        first_name (str): First name of the User
        last_name (str): Last name of the User
        email (str): Email address of the User
        password (str): Password for the User
        is_admin (bool): User is Admin
        places (list[Place]): Places the User owns
    
    Requirements:
        first_name: Required and cannot be longer than 50 characters.
        last_name: Required and cannot be longer than 50 characters.
        email: Required and must be a valid email addresss.
        password: Must contain minimum of 8 characters, a letter, a number and a special character.
        is_admin: Defaults to False.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship Association table (Place > User{owner} reviews > user)
    # Add to the User class
    places = db.relationship('Place', backref='owner', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        super().__init__()

    @validates("password")
    def hash_password(self, key, password):
        """Hashes the password before storing it
        Args: password (str): plaintext password to hash
        Note: bcrypt is used to securely hash the password
        """
        # FAIL SAFE
        if password is None:
            raise ValueError("Password cannot be None")

        # Validate password
        password_check = self.validate_password(password)
        if password_check[0] == False:
            raise password_check[1]

        # Use bcrypt to hash the password
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies the password that was inputted to match the hashed password
        Args: password (str): plaintext password to check
        Returns: boolean [True if match, False otherwise]
        """

        if self.password is None:
            return False
        return bcrypt.check_password_hash(self.password, password)


    def validate_password(self, password):
        """Checks a password is sufficiently secure"""
        special_characters = "!@#$%^&*(){}[]\"'<>,.?|`~;:"
        if len(password) >= 8:
            if all(not c.isalpha() for c in password):
                return (False, ValueError("Password is missing a letter"))
            elif all(not c.isdigit() for c in password):
                return (False, ValueError("Password is missing a digit"))
            elif all(not c in special_characters for c in password):
                return (False, ValueError("Password is missing a special character"))
            return (True, True)
        else:
            return (False, ValueError("Password must be at least 8 characters"))

    def __getitem__(self, key):
        return getattr(self, key)

    @property
    def serialized(self, key):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin':self.is_admin
        }
