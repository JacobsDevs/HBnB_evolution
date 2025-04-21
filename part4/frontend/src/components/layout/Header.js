import React, { useEffect, useState} from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check authentication status whenever the component renders or location changes
  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, [location]); // Add location dependency to re-check when routes change
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setIsAuthenticated(false);
    navigate('/');
  };

  return (
    <header className="header">
      <div className="logo-container">
        <Link to="/">
          <h1>HBnB</h1>
        </Link>
      </div>
      <nav className="navigation">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/places">Places</Link></li>
          {isAuthenticated ? (
            <>
              <li><Link to="/places/add">Add Place</Link></li>
              <li><Link to="/profile/me">Profile</Link></li>
              <li><button onClick={handleLogout} className="logout-btn">Logout</button></li>
            </>
          ) : (
            <li><Link to="/login">Login</Link></li>
          )}
        </ul>
      </nav>
    </header>
  );
};

export default Header;