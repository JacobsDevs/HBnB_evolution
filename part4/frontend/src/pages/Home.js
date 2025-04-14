import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Navigate to the results page with the search query as a URL parameter
      navigate(`/places?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="home-page">
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
      
      <section className="featured-places">
        <h2>Featured Places</h2>
        <div className="places-grid">
          {/* Featured places will go here */}
          <p>Loading featured places...</p>
        </div>
      </section>
      
      <section className="blog-section">
        <h2>From Our Blog</h2>
        <div className="blog-posts">
          {/* Blog posts will go here */}
          <p>Coming soon...</p>
        </div>
      </section>
    </div>
  );
};

export default Home;