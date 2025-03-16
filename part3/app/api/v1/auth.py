from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.extensions import bcrypt

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(require=True, description='User email address'),
    'password': fields.String(required=True, description='User Password')
})

# Model for Token Response when created
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'user_id': fields.String(description='User ID')
})



@api.route('/login')
class Login(Resource):
    """Login page for authentication and authorization"""
    @api.expect(login_model)
    @api.response(200,'Login Successful', token_model)
    @api.response(401,'Authentication failed')
    def post(self):
        """Login to get JWT Token
        Created and stored on client machine"""

        data = request.json

        # Find the user by email
        user = facade.get_user_by_email(data.get('email'))

        # Check if user exists and password is correct
        if user and user.verify_password(data.get('password')):

        # Create token with user identity and admin credentials
        # Admin status in token allows verification of admin privileges
            # >> Having the credentials and status in the token means that
            #   no query is needed or made to the database
            #   for each protected endpoint
            access_token = create_access_token(
                identity=user.id,
                additional_claims={"is_admin": user.is_admin}
            )
            return {
                'access_token': access_token,
                'user_id': user.id
            }, 200

        return {'error': 'Invalid email or password'}, 401

@api.route('/bootstrap')
class BootstrapAdmin(Resource):
    @api.expect(token_model)
    @api.response(201, 'Admin user created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Admin user already exists')
    def post(self):
        """Bootstrap the first admin user (one-time operation)"""
        # Basically check if there is an admin already created if not set first user creation to admin

        all_users = facade.get_all_users()
        admin_exists = any(user.get('is_admin', False) for user in all_users)

        if admin_exists:
            return {'error': 'Admin user already exists. User regular login'}, 409
        
        user_data = api.payload

        user_data['is_admin'] = True

        try:
            new_user = facade.create_user(user_data)
            return {
                'message': 'Admin user created successfully',
                'id': new_user.id,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return{'error': str(e)}, 400

# Check if user is an admin or not (boolean)
# Utility Function (Decorator)
# Remember: >> 'jwt_required() does the authentication
#           and 'claims does the authorization (Does it have the right
#           privileges being "is_admin, TRUE" )
#       *args = Captures positional arguments as tuples '()'
#       **kwargs = Captures keyword arguments as dictionaries '{}'
def admin_required():
    """
    Custom decorator to check if the authenticated user is an admin

    This utility function can be used as a decorator on endpoints that should only be accessible to admins only. is_admin = True

    Returns: Decorated function that checks admin status
    """
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            # Claims is where we get the JWT Token from
            claims = get_jwt()

            if not claims.get('is_admin', False):
                return {'error': 'Admin privilege required'}, 403

            # Return the (Original) function
            return fn(*args, **kwargs)
        return decorator
    return wrapper
