import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './FeaturedPlaces.css';
import api from '../services/api';

const FeaturedPlaces = () => {
  const [featuredPlaces, setFeaturedPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('new');
  
  const categories = [
    { id: 'new', name: 'Newly Added' },
    { id: 'top-rated', name: 'Top Rated' },
    { id: 'popular', name: 'Most Popular' },
    { id: 'unique', name: 'Unique Stays' }
  ];

  useEffect(() => {
    const fetchFeaturedPlaces = async () => {
      setLoading(true);
      try {
        // In a real app, you would have different endpoints for different categories
        // For now, we'll use the same endpoint and filter/sort client-side
        const response = await api.get('/places');
        let places = response.data;
        
        // Apply different sorting/filtering based on category
        switch(activeCategory) {
          case 'new':
            // Sort by creation date (newest first)
            places = places.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            break;
          case 'top-rated':
            // Sort by rating (highest first)
            places = places.filter(place => place.reviews?.length > 0)
              .sort((a, b) => {
                const avgA = a.reviews.reduce((sum, r) => sum + r.rating, 0) / a.reviews.length;
                const avgB = b.reviews.reduce((sum, r) => sum + r.rating, 0) / b.reviews.length;
                return avgB - avgA;
              });
            break;
          case 'popular':
            // Sort by number of reviews (most reviewed first)
            places = places.sort((a, b) => (b.reviews?.length || 0) - (a.reviews?.length || 0));
            break;
          case 'unique':
            // Filter for places with unique amenities
            // This is just a placeholder logic - you would customize based on your data
            places = places.filter(place => place.amenities?.length > 3);
            break;
          default:
            break;
        }
        
        // Limit to 6 places
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
      
      <div className="carousel-container">
        {loading ? (
          <p className="loading-message">Loading featured places...</p>
        ) : featuredPlaces.length > 0 ? (
          <div className="places-carousel">
            {featuredPlaces.map(place => (
              <div className="place-card" key={place.id}>
                <div className="place-image">
                  <div className="placeholder-image"></div>
                </div>
                <div className="place-details">
                  <h3>{place.title}</h3>
                  <p className="place-price">${place.price} / night</p>
                  <p className="place-description">
                    {place.description.substring(0, 60)}...
                  </p>
                  <Link to={`/places/${place.id}`} className="view-details-btn">
                    View Details
                  </Link>
                </div>
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