from flask_restx import Namespace, Resource, fields
from ...services.facade import facade

# Create a namespace for amenities-related endpoints
# Easier to read and identify the page / endpoint
api = Namespace('amenities', description='Amenity Operations')

# Define the amenity model(structure) for input validation and documentation
# Request validation and swagger documentation (web dev use later potentially)
amenity_model = api.model('Amenity', {
    'name': fields.String(require=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    """
    'Resource' class for operations on collection amenities (GET)
    Handles operations that don't require a specific amenity ID:
    - GET: Retrieve ALL amenities
    - POST: Create a new amenity
    """
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Get ALL amenities

        This endpoint gets a list of ALL amenities stored in the system/DB

        Returns:
            tuple: A tuple containing:
                list: List of amenity Dictionaries (dict)
                int: HTTP status code (200 'GREAT SUCCESS')
        """
        # Use the facade to get all amenities (Abstraction later between API and data)
        amenities = facade.get_all_amenities()
        return amenities, 200

@api.expect(amenity_model, validate=True)
@api.response(201,'Amenity successfully created')
@api.response(400, 'Invalid input data')
def post(self):
    """
    Create a new amenity.

    This endpoint creates a new amenity based on the provided data.
    Data must include 'name' field and may(optional) include 'description'

    'name' doesn't exceed 50 characters

    Returns:
        tuple: A tuple containing:
            dict: The created amenity data
            int: HTTP status code (201 for created successfully)

    Raises:
        400 Bad Request: If input validation fails
    """
    # Extract data from the request payload
    amenity_data = api.payload

    try:
        # Use the facade (controller) to create new amenity
        new_amenity = facade.create_amenity(amenity_data)

        # Return created amenity_data with a 201 status code(Created Success)
        return {
            'id': new_amenity,
            'name': new_amenity.name,
            'description': new_amenity.description,
            'created_at':new_amenity.created_at,
            'updated_at': new_amenity.updated_at
        }, 201
    except ValueError as err_msg_create:
        # Handle validation errors from the model
        return {'error message creating amenity': str(err_msg_create)}, 400
