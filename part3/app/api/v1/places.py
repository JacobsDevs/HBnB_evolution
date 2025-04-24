from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.app.services.facade import facade

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
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Creates a new place Authenticated users only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin, False')

        place_data = api.payload

        # Setting owner_id to current authenticated user unless admin is specifying another owner (Changing of hands you could say)
        # Remember >> Only admins can create places for other users
        if 'owner_id' in place_data:
            if not is_admin and place_data['owner_id'] != current_user_id:
                return {"error": "Unauthorized action - cannot create place for another user"}, 403
        else:
            place_data['owner_id'] = current_user_id

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
        place.update({'owner': facade.get_user(place['owner_id']).serialized})
        return place, 200
    
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (For owner or admin only)"""
        # Get ID and admin status (JWT) > Get place > Check if user is_admin > Update info
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404
        
        if not is_admin and place.get('owner_id') != current_user_id:
            return {"error": "Unauthorized action - not the place owner"}, 403

        place_new_data = api.payload

        # Non-Admin users cannot change owner_id information
        if not is_admin and 'owner_id' in place_new_data and place_new_data['owner_id'] != current_user_id:
            return {"error": "Unauthorized action - cannot transfer ownership"}, 403

        try:
            updated_place = facade.update_place(place_id=place_id, place_data=place_new_data)
            return updated_place, 200
        except ValueError:
            return {"error": "Invalid input data"}, 400

    @api.response(204, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if place is None:
            return {"error": "Place not found"}, 404

        if not is_admin and place.get('owner_id') != current_user_id:
            return {"error": "Unauthorized action - not the place owner"}, 403

        success = facade.delete_place(place_id)
        if not success:
            return {"error": "Place not found"}, 404

        return '', 204

@api.route('/<place_id>/amenities')
class PlaceAmenityResource(Resource):
    """
    Resource class for operations on amenities for a specific place.
    """

    @api.response(200, 'List of amenities for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all amenities for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Return amenities from the place
        return place.get('amenities', []), 200

    @api.expect(api.model('AmenityId', {
        'amenity_id': fields.String(required=True, description='ID of the amenity to add')
    }))
    @api.response(200, 'Amenity added to place successfully')
    @api.response(404, 'Place or amenity not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self, place_id):
        """Add an amenity to a place (Owner and Admin Only)"""
        # Do the JWT checks first
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place_obj = facade.get_place(place_id)
        if not place_obj:
            return  {'error': 'Place not found'}, 404
        
        if not is_admin and place_obj.get('owner_id') != current_user_id:
            return {"error": "Unauthorized action - not the place owner"}, 403

        # Extract amenity ID from the request body
        amenity_id = api.payload.get('amenity_id')

        # Debug logging
        # print(f"Adding amenity {amenity_id} to place {place_id}")

        # Use the facade's add_amenity_to_place method
        success = facade.add_amenity_to_place(place_id, amenity_id)

        if not success:
            amenity = facade.get_amenity(amenity_id)

            if not amenity:
                return {'error': 'Amenity not found'}, 404

            return {'error': 'Failed to add amenity to place'}, 500

        return {'message': 'Amenity added to place successfully'}, 200
