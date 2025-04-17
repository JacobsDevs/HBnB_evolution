import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { getAllPlaces } from '../services/api';
import './PlaceResults.css';

const PlaceResults = () => {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();
  const [filters, setFilters] = useState({
    priceMin: '',
    priceMax: '',
    bedrooms: '',
    propertyType: '',
    amenities: []
  });
  const [originalPlaces, setOriginalPlaces] = useState([]);
  
  // Extract search query from URL parameters
  const searchParams = new URLSearchParams(location.search);
  const searchQuery = searchParams.get('search');

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value
    });
  };

  const handleAmenityChange = (amenity) => {
    if (filters.amenities.includes(amenity)) {
      setFilters({
        ...filters,
        amenities: filters.amenities.filter(item => item !== amenity)
      });
    } else {
      setFilters({
        ...filters,
        amenities: [...filters.amenities, amenity]
      });
    }
  };

  const applyFilters = () => {
    // Start with all places or search results
    let filteredPlaces = [...originalPlaces];
    
    // Apply price minimum filter
    if (filters.priceMin) {
      filteredPlaces = filteredPlaces.filter(place => 
        place.price >= parseInt(filters.priceMin)
      );
    }
    
    // Apply price maximum filter
    if (filters.priceMax) {
      filteredPlaces = filteredPlaces.filter(place => 
        place.price <= parseInt(filters.priceMax)
      );
    }
    
    // Apply bedrooms filter
    if (filters.bedrooms) {
      filteredPlaces = filteredPlaces.filter(place => 
        place.bedrooms >= parseInt(filters.bedrooms)
      );
    }
    
    // Apply property type filter
    if (filters.propertyType) {
      filteredPlaces = filteredPlaces.filter(place => 
        place.property_type === filters.propertyType
      );
    }
    
    // Apply amenities filter
    if (filters.amenities.length > 0) {
      filteredPlaces = filteredPlaces.filter(place => 
        filters.amenities.every(amenity => 
          place.amenities && place.amenities.includes(amenity)
        )
      );
    }
    
    // Update the places state with filtered results
    setPlaces(filteredPlaces);
  };

  useEffect(() => {
    // Function to fetch places based on search query
    const fetchPlaces = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch places from API
        const data = await getAllPlaces();
    
        // Filter based on search query if it exists
        if (searchQuery) {
          const filteredPlaces = data.filter(place => 
            place.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
            place.description.toLowerCase().includes(searchQuery.toLowerCase())
          );
          setPlaces(filteredPlaces);
          setOriginalPlaces(filteredPlaces); // Store original search results
        } else {
          setPlaces(data);
          setOriginalPlaces(data); // Store original data
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
  <h2>Filter Results</h2>
  <div className="filter-grid">
    <div className="filter-group">
      <label>Price Range</label>
      <div className="price-range">
        <input
          type="number"
          name="priceMin"
          placeholder="Min"
          value={filters.priceMin}
          onChange={handleFilterChange}
        />
        <span>to</span>
        <input
          type="number"
          name="priceMax"
          placeholder="Max"
          value={filters.priceMax}
          onChange={handleFilterChange}
        />
      </div>
    </div>
    
    <div className="filter-group">
      <label>Bedrooms</label>
      <select
        name="bedrooms"
        value={filters.bedrooms}
        onChange={handleFilterChange}
      >
        <option value="">Any</option>
        <option value="1">1+</option>
        <option value="2">2+</option>
        <option value="3">3+</option>
        <option value="4">4+</option>
      </select>
    </div>
    
    <div className="filter-group">
      <label>Property Type</label>
      <select
        name="propertyType"
        value={filters.propertyType}
        onChange={handleFilterChange}
      >
        <option value="">Any</option>
        <option value="apartment">Apartment</option>
        <option value="house">House</option>
        <option value="villa">Villa</option>
        <option value="cabin">Cabin</option>
      </select>
    </div>
    
    <div className="filter-group amenities-filter">
      <label>Amenities</label>
      <div className="amenities-options">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filters.amenities.includes('wifi')}
            onChange={() => handleAmenityChange('wifi')}
          />
          WiFi
        </label>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filters.amenities.includes('pool')}
            onChange={() => handleAmenityChange('pool')}
          />
          Pool
        </label>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filters.amenities.includes('kitchen')}
            onChange={() => handleAmenityChange('kitchen')}
          />
          Kitchen
        </label>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filters.amenities.includes('parking')}
            onChange={() => handleAmenityChange('parking')}
          />
          Parking
        </label>
      </div>
    </div>
  </div>
  
  <div className="filter-actions">
    <button className="apply-filters-btn" onClick={applyFilters}>
      Apply Filters
    </button>
    <button
      className="clear-filters-btn"
      onClick={() => {
        setFilters({
          priceMin: '',
          priceMax: '',
          bedrooms: '',
          propertyType: '',
          amenities: []
        });
        // Reset to original search results
        setPlaces([...originalPlaces]);
      }}
    >
      Clear Filters
    </button>
  </div>
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