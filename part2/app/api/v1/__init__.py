# Import the amenities namespace
from flask_restx import Api

api = Api(
    title='HBnB API',
    version='1.0',
    description='HBnB Application API',
    doc='/api/v1/'
)

# Import and register namespaces
