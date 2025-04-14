import React from 'react';
import './PlaceResults.css';

const PlaceResults = () => {
  return (
    <div className="place-results-page">
      <h1>Find Your Perfect Place</h1>
      <div className="filter-section">
        {/* Filters will go here */}
        <p>Filters coming soon...</p>
      </div>
      <div className="places-grid">
        {/* Place results will go here */}
        <p>Loading places...</p>
      </div>
    </div>
  );
};

export default PlaceResults;