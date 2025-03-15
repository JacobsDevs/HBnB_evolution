from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Create a namespace for reviews-related endpoints
# Easier to read and identify the page / endpoint
api = Namespace('reviews', description='Review Operations')

# Define the review model(structure) for input validation and documentation
# Request validation and swagger documentation (web dev use later potentially)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Leaving review comment'),
    'rating': fields.Integer(required=True, description='Rating must be between 1 and 5')
    'place_id': fields.String(description='ID of the place being reviewed'),
    'user_id': fields.String(description='ID of the user writing the review'),
})

@api.route('/')
class ReviewList(Resource):
    """
    'Resource' class for operations on collection reviews
    """
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Get ALL reviews

        This endpoint gets a list of ALL reviews stored in the system/DB

        Returns:
            tuple: A tuple containing:
                list: List of review Dictionaries (dict)
                int: HTTP status code (200 'GREAT SUCCESS')
        """
        # Use the facade to get all reviews (Abstraction later between API and data)
        reviews = facade.get_all_reviews()
        return reviews, 200

    @api.expect(review_model, validate=True)
    @api.response(201,'review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized Action')
    @jwt_required()
    def post(self):
        """
        Create a new review.

        This endpoint creates a new review based on the provided data.
            - text (str): Content of the review
            - rating (int): Rating (1-5)
            - place (Place): Place being reviewed
            - user (User): User who wrote the review

        Returns:
            tuple: A tuple containing:
                dict: The created review data
                int: HTTP status code (201 for created successfully)

        Raises:
            400 Bad Request: If input validation fails
        """
        # Always get JWT status
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Extract data from the request payload
        review_data = api.payload

        # If user_id is current user set it, unless Admin authorized if no, set it to the current approved user
        if 'user_id' in review_data:
            if not is_admin and review_data['user_id'] is not current_user_id:
                return {'error': 'Unauthorized action - cannot create review as another user'}, 403
        else:
            review_data['user_id'] = current_user_id

        # See the place being reviewed and make sure the owner isn't reviewing their own place.
        place_id = review_data.get('place_id')
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.get('owner_id') is current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        if not is_admin and facade.has_user_reviewed_place(current_user_id, place_id):
            return {'error': 'You have already reviewed this place'}, 400


        try:
            # Use the facade (controller) to create new review
            new_review = facade.create_review(review_data)

            # Return created review_data with a 201 status code(Created Success)
            return {
                'id': new_review.id,
                'created_at': new_review.created_at,
                'updated_at': new_review.updated_at,
                'text': new_review.text,
                'rating': new_review.rating,
                'place_id': new_review.place.id,
                'user_id': new_review.user.id
            }, 201
        except ValueError as err_msg_create:
            # Handle validation errors from the model
            return {'error message creating review': str(err_msg_create)}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource class for operations on individual reviews.
    Handles operations that require a specific review ID:
    - GET: Retrieve a specific review
    - PUT: Update a specific review
    - DELETE: Remove a specific review
    """

    @api.response(200, 'review details retrieved successfully')
    @api.response(404, 'review not found')
    def get(self, review_id):
        """
        Get review details via ID (UUID)

        This endpoint retrieves details of a specific review by ID

        Args:
            review_id (str): UUID of review

        Returns:
            tuple: A tuple containing:
                - dict: The review data if found
                - int: HTTP status code (200 GREAT SUCCESS)
            
        Raises:
            404 not found: If the review with the given ID doesn't exit
        """

        # Use the facade to get the review by ID
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        # Return the review data with status code
        return {
            'id': review.id,
            'created_at': review.created_at,
            'updated_at': review.updated_at,
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place.id,
            'user_id': review.user.id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200,'review Updated Successfully')
    @api.response(404,'review not found')
    @api.response(400,'Invalid Data input')
    @api.response(403, 'Unauthorized Action')
    @jwt_required()
    def put(self, review_id):
        """
        Update review data

        This endpoint updates an existing review with the provided data.
        The review is identified by its ID.

        Args: 
            review_id (str): UUID of review to update

        Returns: 
            tuple: A tuple containing:
                - dict: the update review data
                - int: HTTP status code (200 = GREAT SUCCESS)

        Raises:
            404 Not found: If review with the given ID doesn't exist
            400 Bad request: If input validation fails
        """

        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin' False)

        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'review doesn\'t exist'}, 404

        # Need to check if the review is the original writer (author) or has admin priv's
        # Non-admins cannot edit the review and or info
        if not is_admin and review.get('user_id') is not current_user_id:
            return {'error': 'Unauthorized action - not the review creator'}, 403

        # Extract the updated data from the request
        update_data = api.payload

        if not is_admin:
            if 'user_id' in update_data and update_data['user_id'] != current_user_id:
                return {'error': 'Unauthorized action - cannot change review author'}, 403
            if 'place_id' in update_data and update_data['place_id'] != review.get('place_id'):
                return {'error': 'Unauthorized action - cannot change reviewed place'}, 403

        try:
            # Use facade to update review
            updated_review = facade.update_review(review_id, update_data)

            # If update successful, return the updated data
            return {
                'id': updated_review.id,
                'created_at': updated_review.created_at,
                'updated_at': updated_review.updated_at,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'place_id': updated_review.place.id,
                'user_id': updated_review.user.id
            }, 200
        except ValueError as e:
            # Handle validation errors from the 'model'
            return {'error': str(e)}, 400

    @api.response(204, 'review successfully deleted')
    @api.response(404, 'review not found')
    @api.response(403, 'Unauthorized Action')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete an review.

        This endpoint removes an review from the system (memory/DB)
        review identified via ID

        args: review_id (str): UUID of review wanting to delete

        Returns:
            tuple: tuple containing:
                - str: Empty string (no content will be shown due to deletion)
                - int: HTTP status code (204 indicating no content delete was a success)

        Raises:
            404 Not Found: If the review ID doesn't exist.
        """
        
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        # You need to check if the review that is getting deleted is the OG writer or Admin Only
        if not is_admin and review.get('user_id') is not current_user_id:
            return {'error': 'Unauthorized action - not the review author'}, 403

        # Use facade to delete the review
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'review doesn\'t exist'}, 404

        # Return status code for deletion
        return '', 204

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource class for operations related to reviews for a specific place.
    - GET: Retrieve all reviews for a specific place
    """
    
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place
        
        This endpoint retrieves all reviews associated with a specific place.
        The place is identified by its ID.
        
        Args:
            place_id (str): UUID of the place
            
        Returns:
            tuple: A tuple containing:
                - list: The list of reviews for the place
                - int: HTTP status code (200 for success)
                
        Raises:
            404 Not Found: If the place with the given ID doesn't exist
        """
        reviews = facade.get_reviews_by_place(place_id)
        
        if reviews is None:
            return {'error': 'Place not found'}, 404
            
        return reviews, 200
    
    @api.expect(review_model)
    @api.response(201, 'Review for place created successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """
        Add a review to a specific place
        
        This endpoint creates a new review associated with a specific place.
        The place is identified by its ID.
        
        Args:
            place_id (str): UUID of the place
            
        Returns:
            tuple: A tuple containing:
                - dict: The created review data
                - int: HTTP status code (201 for created successfully)
                
        Raises:
            404 Not Found: If the place with the given ID doesn't exist
            400 Bad Request: If input validation fails
        """
        # Ensure the place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        # Extract data from the request payload
        review_data = api.payload
        
        # Add the place_id to the review data
        review_data['place_id'] = place_id
        
        try:
            # Create the review using the facade
            new_review = facade.create_review(review_data)
            
            # Return the created review data
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': place_id,
                'created_at': new_review.created_at,
                'updated_at': new_review.updated_at
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

