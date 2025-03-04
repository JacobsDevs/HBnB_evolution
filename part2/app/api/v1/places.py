from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description="Title of the place"),
    'description': fields.String(required=True, description="description of the place"),
    'price': fields.Float(required=True, description="Price per night"),
    'latitude': fields.Float(required=True, description="Latitude of the place"),
    'longitude': fields.Float(required=True, description="Longitude of the place"),
    'owner_id': fields.String(required=True, description="ID of the owner"),
    'amenities': fields.List(fields.String(), required=True, description="List of amenities ID's")   
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Creates a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data=place_data)
            return new_place.serialization(), 201
        except ValueError:
            return {"error": "Invalid input data"}, 400
    
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieves a list of all places"""
        all_places = facade.get_all_places()
        return all_places, 200
    
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID """
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        return place, 200
    
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_new_data = api.payload
        try:
            updated_place = facade.update_place(place_id=place_id, place_data=place_new_data)
            if updated_place is None:
                return {"error": "Place not found"}, 404
            return updated_place, 200
        except ValueError:
            return {"error": "Invalid input data"}, 400
        