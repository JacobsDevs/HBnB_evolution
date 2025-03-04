from flask_restx import Namespace, Resource, fields
from ...services.facade import facade

# Create a namespace for reviews-related endpoints
# Easier to read and identify the page / endpoint
api = Namespace('reviews', description='Review Operations')

# Define the review model(structure) for input validation and documentation
# Request validation and swagger documentation (web dev use later potentially)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Leaving review comment'),
    'rating': fields.Integer(required=True, description='Rating must be between 1 and 5')
})

@api.route('/')
class ReviewList(Resource):
    """
    'Resource' class for operations on collection reviews (GET)
    Handles operations that don't require a specific review ID:
    - GET: Retrieve ALL reviews
    - POST: Create a new review
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
        # Extract data from the request payload
        review_data = api.payload

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
    @api.response(400, 'review not found')
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
        view_review = facade.get_review(review_id)

        if not view_review:
            return {'error': 'review not found'}, 404

        # Return the review data with status code
        return {
            'id': view_review.id,
            'created_at': view_review.created_at,
            'updated_at': view_review.updated_at,
            'text': view_review.text,
            'rating': view_review.rating,
            'place_id': view_review.place.id,
            'user_id': view_review.user.id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200,'review Updated Successfully')
    @api.response(404,'review not found')
    @api.response(400,'Invalid Data input')
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

        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'review doesn\'t exist'}, 404

        # Extract the updated data from the request
        update_data = api.payload

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
        # Use facade to delete the review
        success = facade.delete_review(review_id)

        # If review doesn't exist
        if not success:
            return {'error': 'review doesn\'t exist'}, 404

        # Return status code for deletion
        return '', 204
