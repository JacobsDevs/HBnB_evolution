import pytest



class TestClass():
    def testUserPost(self, client):
        """Creates a user from posted json data"""
        response = client.post("/api/v1/users/", json={
            "first_name": "Jacob",
            "last_name": "Phelan",
            "email": "jacobsdevsmail@gmail.com",
            "password": "abcde123!"
        })
        assert response.json["first_name"] == "Jacob"

    def testUserGetAll(self, client):
        """Gets all users in the user_repo"""
        client.post("/api/v1/users/", json={
            "first_name": "Jacob",
            "last_name": "Phelan",
            "email": "jacobsdevsmail@gmail.com",
            "password": "abcde123!"
        })
        response2 = client.get("api/v1/users/")
        print(type(response2.json))
        assert response2.json[0]['_User__first_name'] == "Jacob"

"""    def testUserGetById(self, client, user):
        \"""Gets a user from the provided id\"""
        response = client.post("/api/v1/users/", json={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password
        })
        id = response.json['id']
        user_id_path = f"/api/v1/users/{id}"
        user = client.get(user_id_path)
        assert user.json['id'] == response.json['id']
        assert user.json['first_name'] == response.json['first_name']
        assert user.json['last_name'] == response.json['last_name']
        assert user.json['email'] == response.json['email']
"""
"""
        Create user
        Get by ID
        Get by parameter
        Get all users
        Update a user
        """
