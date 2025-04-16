import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { getAllPlaces } from '../services/api';
import './PlaceResults.css';

const PlaceResults = () => {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();

  // Extract search query from URL parameters
  const searchParams = new URLSearchParams(location.search);
  const searchQuery = searchParams.get('search');

  useEffect(() => {
    // Function to fetch places based on search query
    const fetchPlaces = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch places from API
        const data = await getAllPlaces();

        // Step Process:
        // If there's a search query, filter the results
        // This assumes the API doesn't have a search parameter
        // If the API supports search, modify the getAllPlaces func to include the query
        if (searchQuery) {
          const filterPlaces = data.filter(place => place.title.toLowerCase().includes(searchQuery.toLowerCase()) || place.description.toLowerCase().includes(searchQuery.toLowerCase()));
          setPlaces(filterPlaces);
        } else {
          setPlaces(data);
        }

        setLoading(false);
      } catch (err) {
        console.error('Error fetching places:', err);
        setError('Failed to fetch places. Please try again later.');
        setLoading(false);
      }
    };

    fetchPlaces();
  }, [searchQuery]); // Re-run when search query changes

  return (
    <div className="place-results-page">
      <h1>
        {searchQuery
          ? `Places matching "${searchQuery}"`
          : 'All Available Places'}
      </h1>

      <div className="filter-section">
        <p>Filter options will be added here</p>
      </div>

      {error && <div className='error-message'>{error}</div>}

      <div className="places-grid">
        {loading ? (
          <p className="loading-message">Searching for places...</p>
        ) : places.length > 0 ? (
          places.map(place => (
            <div key={place.id} className="place-card">
              <div className="place-image">
                {/* Placeholder for place image */}
                <div className="placeholder-image"></div>
              </div>
              <div className="place-details">
                <h3>{place.title}</h3>
                <p className="place-price">${place.price} / night</p>
                <p className="place-description">{place.description.substring(0, 100)}...</p>
                <button className='view-details-btn' onClick={() => window.location.href = `/places/${place.id}`}>
                  View Details
                </button>
              </div>
            </div>
          ))
        ) : (
          <p className="no-results">No places found matching your search.</p>
        )}
      </div>
    </div>
  );
};

export default PlaceResults;
