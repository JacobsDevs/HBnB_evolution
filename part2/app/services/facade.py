from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        try:
            from app.models.user import User
            user = User(user_data)
            self.user_repo.add(user)
        except Exception:
            return "This user data is shit"

    def get_place(self, place_id):
        pass
