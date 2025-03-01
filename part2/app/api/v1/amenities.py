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
                'id': new_amenity.id,
                'name': new_amenity.name,
                'description': new_amenity.description,
                'created_at':new_amenity.created_at,
                'updated_at': new_amenity.updated_at
            }, 201
        except ValueError as err_msg_create:
            # Handle validation errors from the model
            return {'error message creating amenity': str(err_msg_create)}, 400

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource class for operations on individual amenities.
    Handles operations that require a specific amenity ID:
    - GET: Retrieve a specific amenity
    - PUT: Update a specific amenity
    - DELETE: Remove a specific amenity
    """

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(400, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details via ID (UUID)

        This endpoint retrieves details of a specific amenity by ID

        Args:
            amenity_id (str): UUID of amenity

        Returns:
            tuple: A tuple containing:
                - dict: The amenity data if found
                - int: HTTP status code (200 GREAT SUCCESS)
            
        Raises:
            404 not found: If the amenity with the given ID doesn't exit
        """

        # Use the facade to get the amenity by ID
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        # Return the amenity data with status code
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description,
            'created_at': amenity.created_at,
            'updated_at': amenity.updated_at
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200,'Amenity Updated Successfully')
    @api.response(404,'Amenity not found')
    @api.response(400,'Invalid Data input')
    def put(self, amenity_id):
        """
        Update amenity data

        This endpoint updates an existing amenity with the provided data.
        The amenity is identified by its ID.

        Args: 
            amenity_id (str): UUID of amenity to update

        Returns: 
            tuple: A tuple containing:
                - dict: the update amenity data
                - int: HTTP status code (200 = GREAT SUCCESS)

        Raises:
            404 Not found: If amenity with the given ID doesn't exist
            400 Bad request: If input validation fails
        """

        # Check if amenity exists
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity doesn\'t exist'}, 404

        # Extract the updated data from the request
        update_data = api.payload

        try:
            # Use facade to update amenity
            updated_amenity = facade.update_amenity(amenity_id, update_data)

            # If update successful, return the updated data
            if updated_amenity:
                return {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name,
                    'description': updated_amenity.description,
                    'created_at': updated_amenity.created_at,
                    'updated_at': updated_amenity.updated_at
            }, 200
            # else:
            # # Fail safe return
            #     return {'error': 'Amenity doesn\'t exist'}, 404
        except ValueError as e:
        # Handle validation errors from the 'model'
            return {'error': str(e)}, 400


    @api.response(204, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """
        Delete an amenity.

        This endpoint removes an amenity from the system (memory/DB)
        Amenity identified via ID

        args: amenity_id (str): UUID of amenity wanting to delete

        Returns:
            tuple: tuple containing:
                - str: Empty string (no content will be shown due to deletion)
                - int: HTTP status code (204 indicating no content delete was a success)

        Raises:
            404 Not Found: If the amenity ID doesn't exist.
        """
