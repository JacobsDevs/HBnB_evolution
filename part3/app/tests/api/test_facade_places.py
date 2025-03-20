from flask_testing import TestCase
import unittest
from app import create_app, db
from app.models.place import Place
from app.services.facade import facade


class TestPlaceEndpoints(TestCase):

    def create_app(self):
        return create_app(config_name="testing")

    def setUp(self):
        db.create_all()
        test_place = Place("Kamehouse", "Located in the heart of Namekusein", 150.50, 50.25, -160.80, "12345", [])
        db.session.add(test_place)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testPlaceAdd(self):
        # place = Place( "Holberton", "Melbourne School", 100, -37.81712, 144.95926, "12345", [])

        place = {
        "title": "KameHouse",
        "price": 10.10,
        "latitude": 20.20,
        "longitude": 30.30,
        "owner_id": "6789",
        "amenities": [],
        }

        facade.create_place(place)
        got_place = facade.get_place_by_title("KameHouse")
        assert got_place.price == 10.10

#     def testUserAddEndpoint(self):
#         user = {
#             "first_name": "Joe",
#             "last_name": "Jingle",
#             "email": "Joe@jingle.com",
#             "password": "G00d3nough!"
#         }
#         response = self.client.post("/api/v1/users/", json=user)
#         assert response.json['first_name'] == "Joe"
#         assert response.json['last_name'] == "Jingle"

#     def testUserGetByEmail(self):
#         got_user = facade.get_user_by_email("test@user.com")
#         assert got_user['first_name'] == "Test"

#     def testUserGetByName(self):
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         assert got_user['last_name'] == "User"

#     def testUpdateUser(self):
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         facade.update_user(got_user.id, {"last_name": "Updated"})
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         assert got_user['last_name'] == "Updated"

#     def testUpdateUserEndpoint(self):
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         facade.update_user(got_user.id, {"last_name": "Updated"})
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         assert got_user.last_name == "Updated"

#     def testDeleteUser(self):
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         facade.delete_user(got_user.id)
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         assert got_user == None

#     def testDeleteUserEndpoint(self):
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         credentials = {'email': 'test@user.com', 'password': 'Testpass1!'}
#         login = self.client.post("/api/v1/auth/login", json=credentials).json['access_token']
#         response = self.client.delete("/api/v1/users/{}".format(got_user.id), headers={'Authorization': "Bearer {}".format(login)})
#         assert response.status_code == 204
#         got_user = facade.get_user_by_parameter("first_name", "Test")
#         assert got_user == None

if __name__ == "__main__":
    unittest.main()