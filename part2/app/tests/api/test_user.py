import pytest


class TestClass():
    def testUserPost(self, client, user):
        """Creates a user from posted json data"""
        response = client.post("/api/v1/users/", json=user)
        assert response.json["first_name"] == "John"

    def testUserGetAll(self, client, user):
        """Gets all users in the user_repo"""
        response = client.get("api/v1/users/")
        assert response.json[0]['first_name'] == "John"

    def testUserGetById(self, client, user):
        """Gets a user from the provided id"""
        response = client.get("/api/v1/users/")
        assert response.json[0]['first_name'] == "John"
        new_response = client.get("/api/v1/users/{}".format(response.json[0]['id']))
        assert new_response.json['id'] == response.json[0]['id']

    def testUserGetByParameter(self, client, user):
        """Gets a user from the requested parameter
        In this case "email"."""
        response = client.get("/api/v1/user?email={}".format(user.email))
        assert response.json[0]['first_name'] == "John"

"""
        [*] Create user
        [*] Get by ID
        [] Get by parameter
        [*] Get all users
        [] Update a user
"""
