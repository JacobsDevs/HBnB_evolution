import pytest

"""the data on the test is persistant, it means
that once a fixture is created or a test 
has run and POST a place, the next test will have that in memory"""


"""
ToDo's:

1. Test Create place
2. get a place
3. get all places
4. Update a place

"""

class TestClass():
    
    def testPlacesPost(self, client, place):
        """Creates a place from a json post data """
        response = client.post("/api/v1/places/", json=place)
        assert response.json["title"] == "Holberton"
    
    def testPlacesPostError(self, client):
        """Creates a place from a json post data """
        response = client.post("/api/v1/places/", json= {
            "title": "Casa",
            "description": "Colombia",
            "price": -150,
            "latitude":85.81712,
            "longitude":100.95926,
            "amenities": []
        })
        assert response.status_code == 400

    def testGetPlaces(self, client):
        """Gets a list of all places"""
        
        client.post("/api/v1/places/", json={
            "title": "Casa",
            "description": "Colombia",
            "price": 150,
            "latitude": 85.81712,
            "longitude": 100.95926,
            "owner_id": "56789",
            "amenities": []
            })
        response = client.get("/api/v1/places/")
        titles = [p['title'] for p in response.json]
        assert "Holberton" in titles
        assert "Casa" in titles
    
    def testGetPlaceByID(self, client):
        """get a specific place by ID"""
        response = client.get("/api/v1/places/")
        place_id = response.json[1]["id"]
        response1 = client.get(f"/api/v1/places/{place_id}")
        assert response1.json["id"] == place_id
        assert response1.json['title'] == "Casa"
    
    def testGetPlaceByIDError(self, client):
        """get a specific place by ID"""
        place_id = "eb5d8c6c-fe03-42c0-92fc-42c475274783/wrong"
        response = client.get(f"/api/v1/places/{place_id}")
        assert response.status_code == 404

    def testUpdatePlaces(self, client, update):
        """Creates a place from a json post data """
        response = client.get("/api/v1/places/")
        print(response.json)
        place_id = response.json[0]["id"]
        client.put(f"/api/v1/places/{place_id}", json = update )
        response1 = client.get(f"/api/v1/places/{place_id}")
        print(response1.json)
        assert response1.json['title'] == "KameHouse"