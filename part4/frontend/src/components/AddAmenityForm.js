// AddAmenityForm.js - Update to avoid form nesting
import React, { useState } from 'react';
import { createAmenity } from '../services/api';
import './AddAmenityForm.css';

const AddAmenityForm = ({ onAmenityAdded, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Still needed for the button click
    setLoading(true);
    setError('');

    try {
      // Validate
      if (!formData.name.trim()) {
        throw new Error('Amenity name is required');
      }

      // Submit to API
      const newAmenity = await createAmenity(formData);
      
      // Call the callback with the new amenity
      onAmenityAdded(newAmenity);
      
      // Reset form
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
      
      {error && <div className="amenity-error-message">{error}</div>}
      
      {/* Use div instead of form to avoid nesting issues */}
      <div className="amenity-form">
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