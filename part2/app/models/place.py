from app.models.baseModel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=[]): 
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def get_owner(self):
        if database.users.get(self.owner_id) != []:
            return database.users.get(self.owner_id)
        else:
            raise Exception(UserDontExist)




users = {
    'abc': {'name': 'john'}
}

places = {
    'def': {'title': 'smith st',
            'owner_id': 'pqy'}
}
