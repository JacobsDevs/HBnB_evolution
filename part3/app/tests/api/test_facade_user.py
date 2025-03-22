from dns.resolver import query
import pytest
from flask_testing import TestCase
from part3.app import config, create_app, db
from part3.app.models.user import User
from part3.app.services.facade import facade
from werkzeug.datastructures import headers


class TestUserEndpoints(TestCase):

    def create_app(self):
        return create_app(config_name='testing')

    def setUp(self):
        db.create_all()
        test_user = User("Test", "User", "test@user.com", "Testpass1!")
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testUserAdd(self):
        # user = User("John", "Smith", "Johnny_smith@email.com", "G00dP455!")
        user = {
            "first_name": "Joe",
            "last_name": "Jingle",
            "email": "Joe@jingle.com",
            "password": "G00d3nough!"
        }
        facade.create_user(user)
        got_user = facade.get_user_by_email("Joe@jingle.com")
        assert got_user['first_name'] == "Joe"

    def testUserAddEndpoint(self):
        user = {
            "first_name": "Joe",
            "last_name": "Jingle",
            "email": "Joe@jingle.com",
            "password": "G00d3nough!"
        }
        response = self.client.post("/api/v1/users/", json=user)
        assert response.json['first_name'] == "Joe"
        assert response.json['last_name'] == "Jingle"

    def testUserGetByEmail(self):
        got_user = facade.get_user_by_email("test@user.com")
        assert got_user['first_name'] == "Test"

    def testUserGetByName(self):
        got_user = facade.get_user_by_parameter("first_name", "Test")
        assert got_user['last_name'] == "User"

    def testUpdateUser(self):
        got_user = facade.get_user_by_parameter("first_name", "Test")
        facade.update_user(got_user.id, {"last_name": "Updated"})
        got_user = facade.get_user_by_parameter("first_name", "Test")
        assert got_user['last_name'] == "Updated"

    def testUpdateUserEndpoint(self):
        got_user = facade.get_user_by_parameter("first_name", "Test")
        facade.update_user(got_user.id, {"last_name": "Updated"})
        got_user = facade.get_user_by_parameter("first_name", "Test")
        assert got_user.last_name == "Updated"

    def testDeleteUser(self):
        got_user = facade.get_user_by_parameter("first_name", "Test")
        facade.delete_user(got_user.id)
        got_user = facade.get_user_by_parameter("first_name", "Test")
        assert got_user == None

    def testDeleteUserEndpoint(self):
        got_user = facade.get_user_by_parameter("first_name", "Test")
        credentials = {'email': 'test@user.com', 'password': 'Testpass1!'}
        login = self.client.post("/api/v1/auth/login", json=credentials).json['access_token']
        response = self.client.delete("/api/v1/users/{}".format(got_user.id), headers={'Authorization': "Bearer {}".format(login)})
        assert response.status_code == 204
        got_user = facade.get_user_by_parameter("first_name", "Test")
        assert got_user == None
