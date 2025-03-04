from flask import Flask
from flask_restx import Api
from datetime import datetime
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
import json

# """This class is to convert the DateTime object into a string,
# because Flask's JSON Serialization does not automatically handle
# datetiem objects"""

# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             "DateTime to string"
#             return obj.isoformat()
#         return super().default(obj)

def create_app():
    app = Flask(__name__)
    api = Api(app, version=1.0, title='HBnB aPI', description='HBnb Application API')

    #register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    return app
