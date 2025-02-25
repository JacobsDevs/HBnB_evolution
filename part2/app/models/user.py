from app.models.baseModel import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    def __init__(self, first_name=None, last_name=None, email=None, password=None, is_admin=False): 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        super().__init__()

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if value == None:
            raise ValueError("First name is required")
        elif self.validate_string_length(value, 50) is False:
            raise ValueError("First name must be less than 50 characters")
        else:
            self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if value == None:
            raise ValueError("Last name is required")
        elif self.validate_string_length(value, 50) is False:
            raise ValueError("Last name must be less than 50 characters")
        else:
            self.__last_name = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if self.validate_password(value):
            self.__password = value
        else:
            raise ValueError("Password is too weak")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value == None:
            raise ValueError("Email is required")
        elif self.validate_email(value) is False:
            raise ValueError("Email is not valid")
        else:
            self.__email = value

    def add_place(self, place):
        self.places.append(place)

    def validate_string_length(self, string, length):
        return len(string) <= length

    def validate_password(self, password):
        return password != "weak"

    def validate_email(self, email):
        try:
            valid = validate_email(email)
            return True
        except EmailNotValidError as e:
            return False


"""    def add_review_to_place(self, place, review):
        self.reviews.append(review)
        place.add_review(review) """
