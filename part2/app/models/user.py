from typing import Tuple
from app.models.baseModel import BaseModel
from email_validator import validate_email, EmailNotValidError

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
    """
    
    def __init__(self, first_name=None, last_name=None, email=None, password=None, is_admin=False): 
        """Initialize the User with all Attributes listed above.
        Requirements:
            first_name: Required and cannot be longer than 50 characters.
            last_name: Required and cannot be longer than 50 characters.
            email: Required and must be a valid email addresss.
            password: Must contain minimum of 8 characters, a letter, a number and a special character.
            is_admin: Defaults to False.

        Raises:
            first_name: ValueError for too many characters or missing.
            last_name: ValueError for too many characters or missing.
            email: ValueError for missing or EmailNotValidError for invalid email.
            password: ValueError for password too weak.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        super().__init__()

    @property
    def first_name(self):
        """Returns first_name"""
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """Validates the first_name requirements from __init__ docstring"""
        if value == None:
            raise ValueError("First name is required")
        elif self.validate_string_length(value, 50) is False:
            raise ValueError("First name must be less than 50 characters")
        else:
            self.__first_name = value

    @property
    def last_name(self):
        """Returns last_name"""
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """Validates the last_name requirements from __init__ docstring"""
        if value == None:
            raise ValueError("Last name is required")
        elif self.validate_string_length(value, 50) is False:
            raise ValueError("Last name must be less than 50 characters")
        else:
            self.__last_name = value

    @property
    def password(self):
        """Returns password"""
        return self.__password

    @password.setter
    def password(self, value):
        """Validates the password requirements from __init__ docstring"""
        password_check: Tuple = self.validate_password(value)
        if password_check[0] == False:
            raise password_check[1]
        else:
            self.__password = value

    @property
    def email(self):
        """Returns email"""
        return self.__email

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

    def add_place(self, place):
        """Adds a place to the user.places array"""
        self.places.append(place)

    def validate_string_length(self, string, length):
        """Checks a string length against a maximum length"""
        return len(string) <= length

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

    def serialize(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
            "places": self.places
        }

    # def validate_email(self, email):
    #     """Checks an email is valid by RFC Standards using email-validator"""
    #     try:
    #         valid = validate_email(email)
    #         return True
    #     except EmailNotValidError as e:
    #         return False

    # def delete_from_database(self):
    #     """Removes self from the user_repo"""
    #     facade.user_repo.delete(self.id)


"""    def add_review_to_place(self, place, review):
        self.reviews.append(review)
        place.ad_review(review) """
