import React, { useState, useEffect } from 'react';
import { createReview, updateReview } from '../services/api';
import './ReviewForm.css';

const ReviewForm = ({ placeId, onReviewAdded, onReviewUpdated, reviewToEdit = null }) => {
  // State for form data
  const [formData, setFormData] = useState({
    text: '',
    rating: 0, // Default rating
  });

  // State for form submission and UI feedback
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  
  // State for checking if user is authenticated
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // State to track if we're in edit mode
  const [isEditMode, setIsEditMode] = useState(false);

  // Check authentication status when component mounts and
  // populate form data if in edit mode
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
    
    // If we have a review to edit, populate the form and set edit mode
    if (reviewToEdit) {
      setFormData({
        text: reviewToEdit.text || '',
        rating: reviewToEdit.rating || 5
      });
      setIsEditMode(true);
    }
  }, [reviewToEdit]);

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle rating selection
  const handleRatingChange = (newRating) => {
    setFormData({
      ...formData,
      rating: newRating
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      // Validate inputs before submission
      if (!formData.text.trim()) {
        throw new Error('Review text is required');
      }

      let response;
      
      if (isEditMode && reviewToEdit) {
        // If in edit mode, update the existing review
        const reviewData = {
          text: formData.text,
          rating: parseInt(formData.rating)
        };
        
        response = await updateReview(reviewToEdit.id, reviewData);
        
        // Notify parent component that a review was updated
        if (onReviewUpdated) {
          onReviewUpdated(response);
        }
      } else {
        // If in create mode, create a new review
        const reviewData = {
          ...formData,
          place_id: placeId
        };
        
        response = await createReview(reviewData);
        
        // Notify parent component that a new review was added
        if (onReviewAdded) {
          onReviewAdded(response);
        }
      }
      
      // Show success message and reset form if not in edit mode
      setSuccess(true);
      if (!isEditMode) {
        setFormData({
          text: '',
          rating: 0
        });
      }
      
    } catch (err) {
      console.error('Error submitting review:', err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError(err.message || 'An error occurred while submitting your review. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Handle form cancellation in edit mode
  const handleCancel = () => {
    // If we have an onCancel callback, call it
    if (onReviewUpdated) {
      onReviewUpdated(null);
    }
  };

  // Render stars for rating selection
  const renderRatingStars = () => {
    const stars = [];
    
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span
          key={i}
          className={`rating-star ${i <= formData.rating ? 'active' : ''}`}
          onClick={() => handleRatingChange(i)}
        >
          <i className="fas fa-star"></i>
        </span>
      );
    }
    
    return stars;
  };

  return (
    <div className={`review-form-container ${isEditMode ? 'edit-mode' : ''}`}>
      <h3>{isEditMode ? 'Edit Your Review' : 'Write a Review'}</h3>
      
      {!isAuthenticated ? (
        // Show login prompt if user is not authenticated
        <div className="login-prompt">
          <p>Please <a href={`/login?redirect=places/${placeId}`}>login</a> to leave a review.</p>
        </div>
      ) : (
        // Show review form for authenticated users
        <>
          {error && <div className="review-error-message">{error}</div>}
          {success && <div className="review-success-message">
            {isEditMode ? 'Your review has been updated successfully!' : 'Your review has been submitted successfully!'}
          </div>}
          
          <form onSubmit={handleSubmit} className="review-form">
            <div className="form-group rating-group">
              <label>Your Rating</label>
              <div className="rating-stars">
                {renderRatingStars()}
                <span className="rating-value">{formData.rating} out of 5</span>
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="review-text">Your Review</label>
              <textarea
                id="review-text"
                name="text"
                value={formData.text}
                onChange={handleChange}
                required
                disabled={loading}
                rows="4"
                placeholder="Share your experience with this place..."
              ></textarea>
            </div>
            
            <div className="form-actions">
              <button 
                type="submit" 
                className="submit-review-button"
                disabled={loading}
              >
                {loading ? 'Submitting...' : isEditMode ? 'Update Review' : 'Submit Review'}
              </button>
              
              {isEditMode && (
                <button 
                  type="button" 
                  className="cancel-button"
                  onClick={handleCancel}
                  disabled={loading}
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
        </>
      )}
    </div>
  );
};

export default ReviewForm;