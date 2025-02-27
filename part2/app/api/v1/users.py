from flask_restx import Namespace, Resource, fields
from app.services import facade
import json
# Namespace -> Object from wich Users endopoint will inherit API configuration/
api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='first name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User succesfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                }, 201
    def get(self):
        """Get a list of all users"""
        users = facade.get_all_users()
        print(users)
        return users

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieves successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a use by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id,
                'first_name':user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                }, 200
