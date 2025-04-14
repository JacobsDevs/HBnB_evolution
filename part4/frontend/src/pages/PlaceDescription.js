import React from 'react';
import { useParams } from 'react-router-dom';
import './PlaceDescription.css';

const PlaceDescription = () => {
  const { id } = useParams();

  return (
    <div className="place-description-page">
      <h1>Place Details</h1>
      <p>Loading details for place ID: {id}</p>
      <div className="place-gallery">
        {/* Photo gallery will go here */}
      </div>
      <div className="place-content">
        <div className="place-info">
          {/* Place details will go here */}
        </div>
        <div className="reservation-panel">
          {/* Reservation form will go here */}
        </div>
      </div>
      <div className="amenities-section">
        <h2>Amenities</h2>
        {/* Amenities list will go here */}
      </div>
      <div className="reviews-section">
        <h2>Reviews</h2>
        {/* Reviews will go here */}
      </div>
      <div className="owner-profile">
        <h2>Meet the Host</h2>
        {/* Owner info will go here */}
      </div>
    </div>
  );
};

export default PlaceDescription;