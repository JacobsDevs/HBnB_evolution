import React, { useState } from 'react';
import DeleteConfirmationModal from './DeleteConfirmationModal';
import { deleteReview } from '../services/api';
import './ReviewForm.css';

const ReviewItem = ({ 
  review, 
  reviewerName, 
  currentUserId, 
  onEditClick, 
  onReviewDeleted 
}) => {
  // State for deletion confirmation modal
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  
  // Check if current user is the author of this review
  const isAuthor = currentUserId && review.user_id === currentUserId;
  
  // Handle delete confirmation
  const handleDeleteConfirm = async () => {
    setIsDeleting(true);
    try {
      await deleteReview(review.id);
      setShowDeleteModal(false);
      if (onReviewDeleted) {
        onReviewDeleted(review.id);
      }
    } catch (error) {
      console.error('Error deleting review:', error);
      alert('Failed to delete review. Please try again.');
    } finally {
      setIsDeleting(false);
    }
  };
  
  // readable date format
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="review-item">
      <div className="review-header">
        <div className="review-author">By: {reviewerName}</div>
        <div className="review-rating">
          Rating: {review.rating}/5
        </div>
      </div>
      <p className="review-text">{review.text}</p>
      <div className="review-date">Posted on: {formatDate(review.created_at)}</div>
      
      {/* Show edit/delete buttons only if current user is the author */}
      {isAuthor && (
        <div className="review-actions">
          <button 
            className="edit-review-btn"
            onClick={() => onEditClick(review)}
          >
            <i className="fas fa-edit"></i> Edit
          </button>
          <button 
            className="delete-review-btn"
            onClick={() => setShowDeleteModal(true)}
          >
            <i className="fas fa-trash-alt"></i> Delete
          </button>
        </div>
      )}
      
      {/* Delete confirmation modal */}
      {showDeleteModal && (
        <DeleteConfirmationModal
          onConfirm={handleDeleteConfirm}
          onCancel={() => setShowDeleteModal(false)}
          isDeleting={isDeleting}
        />
      )}
    </div>
  );
};

export default ReviewItem;