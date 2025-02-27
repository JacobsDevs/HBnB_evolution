from flask_restx import Namespace, Resource, fields
from ...services.facade import facade

api = Namespace('amenities', description='Amenity Operations')

# Define the amenity model(structure) for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(require=True, description='Name of the amenity')
    'description': fields.String(required=True, description='Description of the amenity')
})

@api.route('/')

@api.route('/<amenity_id>')
