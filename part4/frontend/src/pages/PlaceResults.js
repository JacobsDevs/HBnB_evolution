// This component displays a searchable, filterable list of places with pagination.
// It currently implements client-side filtering and pagination, meaning the 
// entire dataset is fetched once and then manipulated in the browser.

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { getAllPlaces } from '../services/api';
import './PlaceResults.css';
import PlaceCard from '../components/PlaceCard';

const PlaceResults = () => {
  // State variables to manage component data and UI state
  const [places, setPlaces] = useState([]); // Filtered places to display
  const [loading, setLoading] = useState(true); // Loading indicator
  const [error, setError] = useState(null); // Error state
  const location = useLocation(); // Access URL parameters (for search)
  
  // State for filter functionality
  const [filters, setFilters] = useState({
    priceMin: '',
    priceMax: '',
    bedrooms: '',
    propertyType: '',
    amenities: []
  });
  
  // State for pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [placesPerPage] = useState(6); // Number of places per page
  const [originalPlaces, setOriginalPlaces] = useState([]); // Unfiltered places (cache)
  
  // Extract search query from URL parameters
  const searchParams = new URLSearchParams(location.search);
  const searchQuery = searchParams.get('search');

  // Calculate pagination values
  const indexOfLastPlace = currentPage * placesPerPage;
  const indexOfFirstPlace = indexOfLastPlace - placesPerPage;
  
  // This line is performing client-side pagination - it slices the filtered places array
  // to only display the appropriate items for the current page
  const currentPlaces = places.slice(indexOfFirstPlace, indexOfLastPlace);
  
  // Calculate total pages for pagination
  const totalPages = Math.ceil(places.length / placesPerPage);
  
  // Pagination navigation functions
  const goToPreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };
  
  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  // Handle filter input changes
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value
    });
  };

  // Toggle amenity filters
  const handleAmenityChange = (amenity) => {
    // If amenity is already selected, remove it
    if (filters.amenities.includes(amenity)) {
      setFilters({
        ...filters,
        amenities: filters.amenities.filter(item => item !== amenity)
      });
    } else {
      // Otherwise, add it to the selected amenities
      setFilters({
        ...filters,
        amenities: [...filters.amenities, amenity]
      });
    }
  };

  // Apply filters to the places data
  // NOTE: This function performs client-side filtering
  // It filters the already-fetched data instead of requesting filtered data from the server
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
    
    // Apply amenities filter - only include places that have all the selected amenities
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

  // Main data fetching effect
  // This runs when the component mounts or when searchQuery changes
  useEffect(() => {
    // Function to fetch places based on search query
    const fetchPlaces = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch all places from API
        // NOTE: This fetches the entire places dataset in one request
        // In a larger application, this could be optimized to fetch only
        // what's needed with server-side filtering and pagination
        const data = await getAllPlaces();
    
        // Filter based on search query if it exists
        // This performs client-side text search on title and description
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
      
      {/* Filter Panel */}
      <div className="filter-section">
        <h2>Filter Results</h2>
        <div className="filter-grid">
          {/* Price Range Filter */}
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
          
          {/* Bedrooms Filter */}
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
          
          {/* Property Type Filter */}
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
          
          {/* Amenities Filter */}
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
        
        {/* Filter Action Buttons */}
        <div className="filter-actions">
          <button className="apply-filters-btn" onClick={applyFilters}>
            Apply Filters
          </button>
          <button
            className="clear-filters-btn"
            onClick={() => {
              // Reset filters to default values
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

      {/* Error Message Display */}
      {error && <div className='error-message'>{error}</div>}
      
      {/* Places Grid - The main content display */}
      <div className="places-grid">
        {loading ? (
          <p className="loading-message">Searching for places...</p>
        ) : currentPlaces.length > 0 ? (
          // Map through the paginated places array to display place cards
          currentPlaces.map(place => (
            <div className="place-card" key={place.id}>
                <PlaceCard key={place.id} id={place.id} title={place.title} description={place.description} price={place.price} />
              </div>
          ))
        ) : (
          <p className="no-results">No places found matching your search.</p>
        )}
      </div>
      
      {/* Pagination Controls */}
      {!loading && places.length > 0 && (
        <div className="pagination">
          <button 
            onClick={goToPreviousPage} 
            disabled={currentPage === 1}
            className="pagination-button"
          >
            &laquo; Previous 
            {/* the &laquo is the << before the word Previous */}
          </button>
          
          <div className="pagination-info">
            Page {currentPage} of {totalPages}
          </div>
          
          <button 
            onClick={goToNextPage} 
            disabled={currentPage === totalPages}
            className="pagination-button"
          >
            Next &raquo;
            {/* the &laquo is the >> after the word Next */}
          </button>
        </div>
      )}
    </div>
  );
};

export default PlaceResults;