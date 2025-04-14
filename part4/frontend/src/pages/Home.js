import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1>Welcome to HBnB</h1>
          <p>Find your perfect place to stay</p>
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