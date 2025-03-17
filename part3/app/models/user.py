from typing import Tuple
from app.models.baseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
from app.extensions import bcrypt, db
import uuid

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

    @validates("password")
    def hash_password(self, password):
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

    @email.setter
    def email(self, value):
        """Validates the email requirements from __init__ docstring"""
        if value == None:
            raise ValueError("Email is required")
        # elif facade.user_repo.get_by_attribute('email', value) != None:
        #     raise ValueError("Email is not unique")
        # elif self.validate_email(value) is False:
        #     raise EmailNotValidError("Email is not valid")
        else:
            self.__email = value

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
