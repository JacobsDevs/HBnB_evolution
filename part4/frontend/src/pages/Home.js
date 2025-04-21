// This component serves as the landing page of the application.
// It provides a search interface and showcases featured places and blog content.
// The component uses reusable components (FeaturedPlaces and BlogSection) to
// organize the home page content.

import FeaturedPlaces from '../components/FeaturedPlaces';
import BlogSection from '../components/BlogSection';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  // State for the search input field
  const [searchQuery, setSearchQuery] = useState('');
  
  // Navigation hook for redirecting after search
  const navigate = useNavigate();

  // Handle search form submission
  const handleSearch = (e) => {
    e.preventDefault();
    
    // Only navigate if there's a non-empty search term
    if (searchQuery.trim()) {
      // Navigate to the results page with the search query as a URL parameter
      // The encodeURIComponent ensures the search term is properly URL-encoded
      navigate(`/places?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="home-page">
      {/* Hero section with search functionality */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>Welcome to HBnB</h1>
          <p>Find your perfect place to stay</p>
          
          {/* Search Bar */}
          <div className="search-container">
            <form onSubmit={handleSearch} className="search-form">
              <input 
                type="text" 
                placeholder="Search for places..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
              <button type="submit" className="search-button">
                Search
              </button>
            </form>
          </div>
        </div>
      </section>
      
      {/* Featured Places section */}
      {/* This uses the FeaturedPlaces component to display properties in categories */}
      <section className="featured-places-section">
        <h2>Featured Places</h2>
        <FeaturedPlaces />
      </section>
      
      {/* Blog section */}
      {/* This uses the BlogSection component to display blog articles */}
      <section className="blog-section">
        <h2>From Our Blog</h2>
        <BlogSection />
      </section>
    </div>
  );
};

export default Home;