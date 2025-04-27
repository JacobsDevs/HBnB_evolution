import React from 'react';
import './ReviewForm.css';

const DeleteConfirmationModal = ({ onConfirm, onCancel, isDeleting }) => {
  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Delete Review</h3>
        </div>
        <div className="modal-body">
          <p>Are you sure you want to delete this review? This action cannot be undone.</p>
        </div>
        <div className="modal-footer">
          <button 
            className="cancel-modal-button" 
            onClick={onCancel}
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button 
            className="confirm-button" 
            onClick={onConfirm}
            disabled={isDeleting}
          >
            {isDeleting ? 'Deleting...' : 'Delete Review'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmationModal;