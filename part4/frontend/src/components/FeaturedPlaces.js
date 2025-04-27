// This component displays featured place listings in a horizontally scrollable carousel.
// It fetches all places data and then uses client-side filtering/sorting
// to organize places into different categories.

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './FeaturedPlaces.css';
import api from '../services/api';
import PlaceCard from './PlaceCard';

const FeaturedPlaces = () => {
  // State management
  const [featuredPlaces, setFeaturedPlaces] = useState([]);  // Stores the current category's filtered places
  const [loading, setLoading] = useState(true);  // Controls loading indicator
  const [activeCategory, setActiveCategory] = useState('new');  // Currently selected category
  
  // Categories for featured places
  const categories = [
    { id: 'new', name: 'Newly Added' },
    { id: 'top-rated', name: 'Top Rated' },
    { id: 'popular', name: 'Most Popular' },
    { id: 'unique', name: 'Unique Stays' }
  ];

  // This effect runs whenever the activeCategory changes
  useEffect(() => {
    const fetchFeaturedPlaces = async () => {
      setLoading(true);
      try {
        // IMPORTANT: This fetches ALL places in one request
        // In a larger application, this should be replaced with category-specific API endpoints
        // that return pre-filtered data from the server
        const response = await api.get('/places');
        let places = response.data;
        
        // Apply different sorting/filtering based on selected category
        // NOTE: All of this filtering and sorting happens client-side
        // In a production app with large datasets, this would be better done on the server
        // This is a **SWITCH STATEMENT**
        switch(activeCategory) {
          case 'new':
            // Sort by creation date (newest first)
            places = places.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            break;
          case 'top-rated':
            // Sort by rating (highest first)
            // This filters to only include places with reviews and calculates average rating
            places = places.filter(place => place.reviews?.length > 0)
              .sort((a, b) => {
                const avgA = a.reviews.reduce((sum, r) => sum + r.rating, 0) / a.reviews.length;
                const avgB = b.reviews.reduce((sum, r) => sum + r.rating, 0) / b.reviews.length;
                return avgB - avgA;
              });
            break;
          case 'popular':
            // Sort by number of reviews (most reviewed first) as a proxy for popularity
            places = places.sort((a, b) => (b.reviews?.length || 0) - (a.reviews?.length || 0));
            break;
          case 'unique':
            // Filter for places with unique amenities
            // For demo purposes, we're defining "unique" as having more than 3 amenities
            // In a real app, this might use more sophisticated criteria
            places = places.filter(place => place.amenities?.length > 3);
            break;
          default:
            break;
        }
        
        // Limit to 6 places to prevent carousel overload
        setFeaturedPlaces(places.slice(0, 6));
        setLoading(false);
      } catch (error) {
        console.error('Error fetching featured places:', error);
        setLoading(false);
      }
    };

    fetchFeaturedPlaces();
  }, [activeCategory]); // Re-fetch when category changes

  return (
    <div className="featured-places-container">
      {/* Category selection tabs */}
      <div className="category-tabs">
        {categories.map(category => (
          <button
            key={category.id}
            className={`category-tab ${activeCategory === category.id ? 'active' : ''}`}
            onClick={() => setActiveCategory(category.id)}
          >
            {category.name}
          </button>
        ))}
      </div>
      
      {/* Carousel container */}
      <div className="carousel-container">
        {loading ? (
          <p className="loading-message">Loading featured places...</p>
        ) : featuredPlaces.length > 0 ? (
          <div className="places-carousel">
            {/* Map through the filtered featured places */}
            {featuredPlaces.map(place => (
              <div className="place-card" key={place.id}>
                <PlaceCard key={place.id} id={place.id} title={place.title} description={place.description} price={place.price} />
              </div>
            ))}
          </div>
        ) : (
          <p className="no-places">No places found in this category.</p>
        )}
      </div>
    </div>
  );
};

export default FeaturedPlaces;