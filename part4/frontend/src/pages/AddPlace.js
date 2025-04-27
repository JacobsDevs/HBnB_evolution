// This component provides a form for users to create a new place listing.
// It handles form state, user input, amenity selection, and API submission.
// The component also includes authentication checks to ensure only logged-in users can add places.

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPlace, getAllAmenities, getUserProfile } from '../services/api';
import AddAmenityForm from '../components/AddAmenityForm';
import './AddPlace.css';
import PlaceSearch from '../components/PlaceSearchComponent';

const AddPlace = () => {
  // React Router's navigation hook for redirection
  const navigate = useNavigate();

  // State management variables
  const [loading, setLoading] = useState(false);  // Controls loading state during API calls
  const [error, setError] = useState('');  // Stores error messages
  const [success, setSuccess] = useState('');  // Stores success messages
  const [amenities, setAmenities] = useState([]);  // All available amenities
  const [selectedAmenities, setSelectedAmenities] = useState([]);  // User's selected amenities
  const [showAddAmenityForm, setShowAddAmenityForm] = useState(false);  // Controls visibility of add amenity form

  // Form data state for the new place
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    latitude: '',
    longitude: '',
    amenities: []  // This is replaced by selectedAmenities when submitting
  });

  // Authentication and amenities loading effect
  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');

    // If not logged in, redirect to login page with return URL
    if (!token || !userId) {
      navigate('/login?redirect=add-place');
      return;
    }

    // Verify that the stored token is valid by making an API call
    const checkAuth = async () => {
      try {
        // Use the stored userId to verify token is valid
        await getUserProfile(userId);
      } catch (err) {
        // If token is invalid (401 error), redirect to login
        if (err.response && err.response.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('userId');
          navigate('/login?redirect=add-place&message=session_expired');
        }
      }
    };

    checkAuth();

    // Fetch available amenities for the selection list
    const fetchAmenities = async () => {
      try {
        const amenitiesData = await getAllAmenities();
        setAmenities(amenitiesData);
      } catch (err) {
        console.error('Error fetching amenities:', err);
        setError('Failed to load amenities. Please try again later.');
      }
    };

    fetchAmenities();
  }, [navigate]);  // Only run on initial render and when navigate changes

  // Handle adding a new amenity
  const handleNewAmenity = (newAmenity) => {
    // Add the new amenity to the amenities list
    setAmenities([...amenities, newAmenity]);

    // Automatically select the newly added amenity
    setSelectedAmenities([...selectedAmenities, newAmenity.id]);

    // Hide the add amenity form
    setShowAddAmenityForm(false);
  };

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle amenity selection toggling
  const handleAmenityToggle = (amenityId) => {
    if (selectedAmenities.includes(amenityId)) {
      // Remove amenity if already selected
      setSelectedAmenities(selectedAmenities.filter(id => id !== amenityId));
    } else {
      // Add amenity if not selected
      setSelectedAmenities([...selectedAmenities, amenityId]);
    }
  };

  const api_key = async () => {
    const data = await process.env.GOOGLE_API_KEY;
    return data
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Prepare place data with selected amenities
      // Convert string values to appropriate types
      const placeData = {
        ...formData,
        price: parseFloat(formData.price),  // Convert price to float
        latitude: parseFloat(formData.latitude),  // Convert latitude to float
        longitude: parseFloat(formData.longitude),  // Convert longitude to float
        amenities: selectedAmenities  // Use the selectedAmenities array for submission
      };

      // Submit the place data to API
      const response = await createPlace(placeData);
      setSuccess('Place created successfully!');

      // Redirect to the newly created place after a short delay
      setTimeout(() => {
        navigate(`/places/${response.id}`);
      }, 2000);
    } catch (err) {
      console.error('Error creating place:', err);
      // Display the error from the API if available
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('An error occurred while creating your place. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-place-page">
      <div className="add-place-container">
        <h1>Add Your Place</h1>

        {/* Error and success message display */}
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Place creation form */}
        <form onSubmit={handleSubmit} className="add-place-form">
          {/* Title field */}
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              disabled={loading}
              placeholder="Enter a catchy title for your place"
            />
          </div>

          {/* Description field */}
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              disabled={loading}
              placeholder="Describe your place, amenities, surroundings, etc."
              rows="5"
            />
          </div>

          {/* Price field */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="price">Price per Night ($)</label>
              <input
                type="number"
                id="price"
                name="price"
                value={formData.price}
                onChange={handleChange}
                required
                disabled={loading}
                min="0"
                step="0.01"
                placeholder="149.99"
              />
            </div>
          </div>

          {/* Location fields (latitude/longitude) */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="latitude">Latitude</label>
              <input
                type="number"
                id="latitude"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                required
                disabled={loading}
                step="any"
                min="-90"
                max="90"
                placeholder="34.0522"
              />
            </div>

            <div className="form-group">
              <label htmlFor="longitude">Longitude</label>
              <input
                type="number"
                id="longitude"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                required
                disabled={loading}
                step="any"
                min="-180"
                max="180"
                placeholder="-118.2437"
              />
            </div>
          </div>

          {/* <PlaceSearch /> */}

          {/* Amenities selection section */}
          <div className="form-group amenities-section">
            <div className="amenities-header">
              <label>Select Amenities</label>
              <button
                type="button"
                className="add-new-amenity-btn"
                onClick={() => setShowAddAmenityForm(!showAddAmenityForm)}
                disabled={loading}
              >
                {showAddAmenityForm ? 'Cancel' : '+ Add New Amenity'}
              </button>
            </div>

            {/* Conditionally show the add amenity form or the amenities selection grid */}
            {showAddAmenityForm ? (
              <AddAmenityForm
                onAmenityAdded={handleNewAmenity}
                onCancel={() => setShowAddAmenityForm(false)}
              />
            ) : (
              <div className="amenities-grid">
                {amenities.length > 0 ? (
                  amenities.map(amenity => (
                    <div className="amenity-item" key={amenity.id}>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={selectedAmenities.includes(amenity.id)}
                          onChange={() => handleAmenityToggle(amenity.id)}
                          disabled={loading}
                        />
                        <span>{amenity.name}</span>
                      </label>
                    </div>
                  ))
                ) : (
                  <p className="no-amenities">Loading amenities...</p>
                )}
              </div>
            )}
          </div>

          {/* Form action buttons */}
          <div className="form-actions">
            <button
              type="submit"
              className="submit-button"
              disabled={loading}
            >
              {loading ? 'Creating Place...' : 'Create Place'}
            </button>
            <button
              type="button"
              className="cancel-button"
              onClick={() => navigate('/places')}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddPlace;
