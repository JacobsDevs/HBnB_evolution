from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx.postman import clean
from app.services import facade
from app.api.v1.auth import admin_required
import json


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='first name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password the user authentication'),
    'is_admin': fields.Boolean(description='Admin privileges flag')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='first name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address of the user'),
    'password': fields.String(description='Password the user authentication'),
    'is_admin': fields.Boolean(description='Admin privileges flag')
})

parser = reqparse.RequestParser()
parser.add_argument('first_name', location='args')
parser.add_argument('last_name', location='args')
parser.add_argument('email', location='args')

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
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

    @api.expect(parser)
    @jwt_required() # Only Authenticated users can view this list
    def get(self):
        """Get a list of all users for Admin Only users"""
        # Check if the current user attempting to access list is admin or not
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': 'Admin privileges required to view all users'}, 403

        query_args = parser.parse_args()
        clean_args = {k: v  for (k, v) in query_args.items() if v != None}
        if clean_args == {}:
            users = facade.get_all_users()
            return users, 200
        elif len(clean_args.keys()) == 1:
            user = facade.get_user_by_parameter(sorted(clean_args.keys())[0], sorted(clean_args.values())[0])
            if user:
                return {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_admin': user.is_admin
                }, 200
            else:
                return {'error': 'User not found'}, 404

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieves successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Retrieve a use by ID (Admin Only)"""
        # Get current user ID and Admin Status to verify request
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin and current_user_id is not user_id:
            return {'error': 'Unauthorized access to other user\'s data'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user information (Authorized user or Admin Only)"""
        # Admin check and authorization check
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin and current_user_id is not user_id:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        # Non-admin users can still update their own information
        if not is_admin:
            if 'email' in user_data or 'password' in user_data or 'is_admin' in user_data:
                return {'error': 'Regular users cannot modify email, password or admin status'}, 403

        user = facade.update_user(user_id, user_data)
        if user is None:
            return {'error': 'User not found'}, 404
        elif user is False:
            return {'error': 'Input data invalid'}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.response(204, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @admin_required()
    def delete(self, user_id):
        """Delete a user (Admin Only)"""
        success = facade.delete_user(user_id)
        if not success:
            return {'error': 'User not found'}, 404

        return '', 204
