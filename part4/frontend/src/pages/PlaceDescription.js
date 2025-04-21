import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getPlaceById } from '../services/api';
import './PlaceDescription.css';

const PlaceDescription = () => {
  const { id } = useParams();
  const [place, setPlace] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlaceDetails = async () => {
      try {
        setLoading(true);
        const placeData = await getPlaceById(id);
        setPlace(placeData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching place details:', err);
        setError('Failed to load place details. Please try again later.');
        setLoading(false);
      }
    };

    fetchPlaceDetails();
  }, [id]);

  if (loading) {
    return <div className="loading-container">Loading place details...</div>;
  }

  if (error) {
    return <div className="error-container">{error}</div>;
  }

  if (!place) {
    return <div className="error-container">Place not found</div>;
  }

  return (
    <div className="place-description-page">
      <h1>{place.title}</h1>

      <div className="place-gallery">
        <div className="placeholder-gallery">
          <p>No photos available</p>
        </div>
      </div>

      <div className="place-content">
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

      <div className="amenities-section">
        <h2>Amenities</h2>
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

      <div className="reviews-section">
        <h2>Reviews</h2>
        {place.reviews && place.reviews.length > 0 ? (
          <div className="reviews-list">
            {place.reviews.map(review => (
              <div className="review-item" key={review.id}>
                <div className="review-header">
                  <div className="review-author">By: {review.user_id}</div>
                  <div className="review-rating">
                    Rating: {review.rating}/5
                  </div>
                </div>
                <p className="review-text">{review.text}</p>
                <div className="review-date">Posted on: {new Date(review.created_at).toLocaleDateString()}</div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data-message">No reviews yet. Be the first to leave a review!</p>
        )}
      </div>

      <div className="owner-profile">
        <h2>Meet the Host</h2>
        {place.owner_id ? (
          <div className="host-info">
            <div className="host-placeholder-image"></div>
            <div className="host-details">
              <p>Host ID: {place.owner_id}</p>
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