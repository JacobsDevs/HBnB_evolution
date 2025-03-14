from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.extensions import bcrypt

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(require=True, description='User email address'),
    'password': fields.String(required=True, descreiption='User Password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200,'Login Successful')
    @api.response(401,'Authentication failed')
    def post(self):

        # Find the user by email 

        # Check if user exists and password is correct

        # Create token with user identity and admin credentials

        # Admin status in token allows verification of admin privileges
            # >> Having the credentials and status in the token means that
            #   no query is needed or made to the database
            #   for each protected endpoint


# Check if user is an admin or not (boolean)

