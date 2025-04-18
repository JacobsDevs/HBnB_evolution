from dns.resolver import query
import pytest


class TestUserEndpoints():
    def testUserPost(self, client, user):
        """Creates a user from posted json data"""
        response = client.post("/api/v1/users/", json=user)
        assert response.json["first_name"] == "John"

    def testUserGetAll(self, client):
        """Gets all users in the user_repo"""
        response = client.get("api/v1/users/")
        assert response.json[0]['first_name'] == "John"

    def testUserGetById(self, client):
        """Gets a user from the provided id"""
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        assert response.json[0]['first_name'] == "John"
        new_response = client.get("/api/v1/users/{}".format(response.json[0]['id']))
        assert new_response.json['id'] == response.json[0]['id']

    def testUserGetByParameter(self, client):
        """Gets a user from the requested parameter"""
        response = client.get("/api/v1/users/", query_string={'email': 'john@smith.com'})
        assert response.status_code == 200
        assert response.json['first_name'] == "John"
        response = client.get("/api/v1/users/", query_string={'first_name': 'James'})
        assert response.status_code == 404
        assert response.json['error'] == 'User not found'
        response = client.get("/api/v1/users/", query_string={'first_name': 'John'})
        assert response.status_code == 200
        assert response.json['first_name'] == 'John'

    def testUserUpdateParameters(self, client, user):
        response = client.get("/api/v1/users/", query_string={'first_name': "John"})
        id = response.json['id']
        address = "/api/v1/users/{}".format(id)
        response = client.put(address, json={'first_name': 'Jason'})
        assert response.status_code == 200
        response = client.get(address)
        assert response.json['first_name'] == 'Jason'
        assert response.json['email'] == 'john@smith.com'
        assert response.status_code == 200

    def testUserUpdateInvalidParameters(self, client, user):
        response = client.get("/api/v1/users/", query_string={'email': "john@smith.com"})
        print(response.json)
        id = response.json['id']
        address = "/api/v1/users/{}".format(id)
        response = client.put(address, json={'name': 'Jason'})
        assert response.status_code == 400

    def testUserUpdateUserDoesNotExist(self, client, user):
        response = client.put("/api/v1/users/ABC", json={'first_name': 'Jason'})
        assert response.status_code == 404

"""
        [*] Create user
        [*] Get by ID
        [*] Get by parameter
        [*] Get all users
        [*] Update a user
"""
