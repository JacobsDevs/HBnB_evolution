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
