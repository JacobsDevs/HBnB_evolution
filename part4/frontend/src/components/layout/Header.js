// This component renders the application's navigation header.
// It displays the logo, navigation links, and handles user authentication state.
// The navigation options change based on whether a user is logged in or not.

import React, { useEffect, useState} from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
  // React Router hooks for navigation and location awareness
  const navigate = useNavigate();
  const location = useLocation();
  
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check authentication status whenever the component renders or location changes
  // We check on location change to ensure the navigation updates if a user logs in/out
  useEffect(() => {
    // Check if user is logged in by looking for auth token in localStorage
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token); // Convert token to boolean (true if exists, false if null/undefined)
  }, [location]); // Add location dependency to re-check when routes change
  
  // Handle user logout
  const handleLogout = () => {
    // Remove authentication data from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    
    // Update authenticated state
    setIsAuthenticated(false);
    
    // Redirect to home page
    navigate('/');
  };

  return (
    <header className="header">
      {/* Logo/Brand section */}
      <div className="logo-container">
        <Link to="/">
          <h1>HBnB</h1>
        </Link>
      </div>
      
      {/* Navigation links */}
      <nav className="navigation">
        <ul>
          {/* Always visible links */}
          <li><Link to="/">Home</Link></li>
          <li><Link to="/places">Places</Link></li>
          
          {/* Conditional rendering based on authentication status */}
          {isAuthenticated ? (
            // Show these links only when user is logged in
            <>
              <li><Link to="/places/add">Add Place</Link></li>
              <li><Link to="/profile/me">Profile</Link></li>
              <li><button onClick={handleLogout} className="logout-btn">Logout</button></li>
            </>
          ) : (
            // Show login link when user is not logged in
            <li><Link to="/login">Login</Link></li>
          )}
        </ul>
      </nav>
    </header>
  );
};

export default Header;