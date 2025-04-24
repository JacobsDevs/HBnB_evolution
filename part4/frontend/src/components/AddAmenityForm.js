// This component provides a form for adding new amenities.
// It's designed to be used inside other forms (particularly the AddPlace form)
// and avoids form nesting issues by using button click handlers instead of form submission.

import React, { useState } from 'react';
import { createAmenity } from '../services/api';
import './AddAmenityForm.css';

const AddAmenityForm = ({ onAmenityAdded, onCancel }) => {
  // State for form inputs
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  
  // State for loading and error handling
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle form submission
  // Note: This is triggered by a button click, not a form submit event
  // This approach avoids issues with nested forms in the parent component
  const handleSubmit = async (e) => {
    e.preventDefault(); // Still needed for the button click
    setLoading(true);
    setError('');

    try {
      // Basic validation
      if (!formData.name.trim()) {
        throw new Error('Amenity name is required');
      }

      // Submit to API using the createAmenity function from our API service
      const newAmenity = await createAmenity(formData);
      
      // Call the callback with the new amenity
      // This allows the parent component to update its state with the new amenity
      onAmenityAdded(newAmenity);
      
      // Reset form to initial state
      setFormData({
        name: '',
        description: ''
      });
      
    } catch (err) {
      console.error('Error creating amenity:', err);
      setError(err.message || 'Failed to create amenity. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-amenity-form-container">
      <h3>Add New Amenity</h3>
      
      {/* Display error message if there is one */}
      {error && <div className="amenity-error-message">{error}</div>}
      
      {/* 
        Important: This is using a div instead of a form element
        This is intentional to avoid nesting form elements in the parent component
        which can cause submission issues in browsers
      */}
      <div className="amenity-form">
        {/* Name input field */}
        <div className="amenity-form-group">
          <label htmlFor="amenity-name">Name</label>
          <input
            type="text"
            id="amenity-name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            disabled={loading}
            placeholder="e.g., Swimming Pool, Gym, etc."
          />
        </div>
        
        {/* Description input field */}
        <div className="amenity-form-group">
          <label htmlFor="amenity-description">Description</label>
          <textarea
            id="amenity-description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            disabled={loading}
            placeholder="Describe the amenity (optional)"
            rows="3"
          />
        </div>
        
        {/* Action buttons */}
        <div className="amenity-form-actions">
          <button 
            type="button" // Changed from submit to button
            className="add-amenity-button"
            onClick={handleSubmit} // Handle submission with onClick
            disabled={loading}
          >
            {loading ? 'Adding...' : 'Add Amenity'}
          </button>
          <button 
            type="button" 
            className="cancel-amenity-button"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddAmenityForm;