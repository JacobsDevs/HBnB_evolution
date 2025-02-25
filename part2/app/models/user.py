from app.models.baseModel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin): 
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        if self.validate_password(password):
            self.password = password
        else:
            raise Exception
        self.is_admin = is_admin
        self.places = []

    def add_place(self, place):
        self.places.append(place)

    def validate_password(self, password):
        if password == "weak":
            raise Exception

"""    def add_review_to_place(self, place, review):
        self.reviews.append(review)
        place.add_review(review) """
