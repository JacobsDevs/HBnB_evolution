// This component displays detailed information about a specific place listing.
// It fetches place data, owner information, and reviewer details to create a
// comprehensive view of the place with reviews and amenities.

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getPlaceById, getUserProfile } from '../services/api';
import './PlaceDescription.css';

const PlaceDescription = () => {
  // Extract place ID from URL parameters
  const { id } = useParams();
  
  // State variables
  const [place, setPlace] = useState(null);  // The place data
  const [owner, setOwner] = useState(null);  // Place owner information
  const [reviewers, setReviewers] = useState({});  // Map of user IDs to reviewer information
  const [loading, setLoading] = useState(true);  // Loading state
  const [error, setError] = useState(null);  // Error state

  // Fetch place details when component mounts or ID changes
  useEffect(() => {
    const fetchPlaceDetails = async () => {
      try {
        setLoading(true);
        
        // Fetch the place data by ID
        const placeData = await getPlaceById(id);
        setPlace(placeData);
        
        // After getting place data, fetch owner information
        if (placeData.owner_id) {
          try {
            const ownerData = await getUserProfile(placeData.owner_id);
            setOwner(ownerData);
          } catch (ownerError) {
            console.error('Error fetching owner details:', ownerError);
            // We don't set the main error state here because the place data loaded successfully
            // This is a non-critical error that shouldn't prevent the user from viewing the place
          }
        }
        
        // If the place has reviews, fetch reviewer information for each unique reviewer
        // This demonstrates client-side data enrichment - we're fetching related data to enhance
        // the user experience (showing reviewer names instead of just IDs)
        if (placeData.reviews && placeData.reviews.length > 0) {
          // Get unique reviewer IDs to avoid duplicate API calls
          const uniqueReviewerIds = [...new Set(placeData.reviews.map(review => review.user_id))];
          const reviewersData = {};
          
          // Use Promise.all to fetch all reviewer data in parallel
          // This is more efficient than sequential requests
          await Promise.all(uniqueReviewerIds.map(async (userId) => {
            try {
              const userData = await getUserProfile(userId);
              reviewersData[userId] = userData;
            } catch (reviewerError) {
              console.error(`Error fetching reviewer ${userId} details:`, reviewerError);
              // Again, not a critical error - we can display reviews without reviewer details if needed
            }
          }));
          
          setReviewers(reviewersData);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching place details:', err);
        setError('Failed to load place details. Please try again later.');
        setLoading(false);
      }
    };

    fetchPlaceDetails();
  }, [id]); // Re-run when place ID changes

  // Show loading state while data is being fetched
  if (loading) {
    return <div className="loading-container">Loading place details...</div>;
  }

  // Show error state if place data couldn't be loaded
  if (error) {
    return <div className="error-container">{error}</div>;
  }

  // Show error if place not found
  if (!place) {
    return <div className="error-container">Place not found</div>;
  }

  // Main component rendering with place data
  return (
    <div className="place-description-page">
      <h1>{place.title}</h1>

      {/* Image gallery - currently a placeholder */}
      <div className="place-gallery">
        <div className="placeholder-gallery">
          <p>No photos available</p>
        </div>
      </div>

      {/* Main content area with place info and booking panel */}
      <div className="place-content">
        {/* Left column - Place information */}
        <div className="place-info">
          <h2>Description</h2>
          <p>{place.description}</p>
          
          <div className="location-info">
            <h3>Location</h3>
            <p>
              <i className="fas fa-map-marker-alt"></i> Coordinates: {place.latitude}, {place.longitude}
            </p>
          </div>
        </div>

        {/* Right column - Booking information */}
        <div className="reservation-panel">
          <h2>Booking Information</h2>
          <div className="price-section">
            <span className="price-amount">${place.price}</span> per night
          </div>
          <button className="book-now-btn">Book Now</button>
          
          <div className="reservation-details">
            <p>Contact the host for availability.</p>
            <p>Check-in time: 3:00 PM</p>
            <p>Check-out time: 11:00 AM</p>
          </div>
        </div>
      </div>

      {/* Amenities section */}
      <div className="amenities-section">
        <h2>Amenities</h2>
        {/* Conditional rendering based on whether amenities exist */}
        {place.amenities && place.amenities.length > 0 ? (
          <div className="amenities-list">
            {place.amenities.map(amenity => (
              <div className="amenity-item" key={amenity.id}>
                <i className="fas fa-check"></i> {amenity.name}
                {amenity.description && <p className="amenity-description">{amenity.description}</p>}
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data-message">No amenities listed for this place.</p>
        )}
      </div>

      {/* Reviews section */}
      <div className="reviews-section">
        <h2>Reviews</h2>
        {place.reviews && place.reviews.length > 0 ? (
          <div className="reviews-list">
            {/* Map through reviews and display with reviewer information if available */}
            {place.reviews.map(review => {
              // Try to get reviewer information, fallback to "Anonymous" if not available
              const reviewer = reviewers[review.user_id];
              const reviewerName = reviewer 
                ? `${reviewer.first_name} ${reviewer.last_name}`
                : 'Anonymous User';
                
              return (
                <div className="review-item" key={review.id}>
                  <div className="review-header">
                    <div className="review-author">By: {reviewerName}</div>
                    <div className="review-rating">
                      Rating: {review.rating}/5
                    </div>
                  </div>
                  <p className="review-text">{review.text}</p>
                  <div className="review-date">Posted on: {new Date(review.created_at).toLocaleDateString()}</div>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="no-data-message">No reviews yet. Be the first to leave a review!</p>
        )}
      </div>

      {/* Host profile section */}
      <div className="owner-profile">
        <h2>Meet the Host</h2>
        {place.owner_id ? (
          <div className="host-info">
            <div className="host-placeholder-image"></div>
            <div className="host-details">
              {/* Display owner information if available */}
              {owner ? (
                <>
                  <h3>{owner.first_name} {owner.last_name}</h3>
                  {owner.email && (
                    <p className="host-email">Contact: {owner.email}</p>
                  )}
                </>
              ) : (
                <p>Host ID: {place.owner_id}</p>
              )}
              <Link to={`/profile/${place.owner_id}`} className="view-profile-btn">
                View Host Profile
              </Link>
            </div>
          </div>
        ) : (
          <p className="no-data-message">Host information unavailable.</p>
        )}
      </div>
    </div>
  );
};

export default PlaceDescription;