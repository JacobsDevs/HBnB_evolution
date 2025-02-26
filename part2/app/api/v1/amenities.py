from flask import request
from flask_restx import Namespace, Resource, fields
from part2.app.services.facade import HBnBFacade

# Create a facade instance to interact with the business logic layer
facade = HBnBFacade()

# Create a namespace for amenities endpoints
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
# This helps Flask-RESTx validate incoming data and generate API documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})

# Define the model for amenity responses to document what the API returns
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier for the amenity'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity'),
    'created_at': fields.DateTime(description='Timestamp when the amenity was created'),
    'updated_at': fields.DateTime(description='Timestamp when the amenity was last updated')
})

@api.route('/')
class AmenityList(Resource):
    """Resource for handling operations on the collection of amenities"""
    
    @api.expect(amenity_model)  # Expect data matching the amenity model
    @api.marshal_with(amenity_response_model, code=201)  # Format response according to model
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity
        
        This endpoint allows creating a new amenity with a name and optional description.
        """
        try:
            # Get JSON data from the request
            amenity_data = request.json
            
            # Create the amenity using the facade
            amenity = facade.create_amenity(amenity_data)
            
            # Return the created amenity with a 201 Created status code
            return amenity.to_dict(), 201
            
        except ValueError as e:
            # Handle validation errors
            api.abort(400, str(e))

    @api.marshal_with(amenity_response_model, as_list=True)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities
        
        This endpoint returns a list of all amenities in the system.
        """
        # Get all amenities using the facade
        amenities = facade.get_all_amenities()
        
        # Convert each amenity to dictionary format
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The unique identifier of the amenity')
class AmenityResource(Resource):
    """Resource for handling operations on a specific amenity"""
    
    @api.marshal_with(amenity_response_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID
        
        This endpoint retrieves the details of a specific amenity.
        """
        # Get the amenity using the facade
        amenity = facade.get_amenity(amenity_id)
        
        # If the amenity doesn't exist, return a 404 Not Found
        if not amenity:
            api.abort(404, f"Amenity with ID {amenity_id} not found")
        
        # Return the amenity details
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.marshal_with(amenity_response_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity's information
        
        This endpoint updates the details of a specific amenity.
        """
        try:
            # Get JSON data from the request
            amenity_data = request.json
            
            # Update the amenity using the facade
            amenity = facade.update_amenity(amenity_id, amenity_data)
            
            # Return the updated amenity
            return amenity.to_dict(), 200
            
        except ValueError as e:
            # Check if this is a "not found" error
            if "not found" in str(e).lower():
                api.abort(404, str(e))
            else:
                # Other validation errors
                api.abort(400, str(e))