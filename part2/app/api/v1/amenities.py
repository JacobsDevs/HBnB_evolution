from flask_restx import Namespace, Resource, fields
# from ...services.facade import facade

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
