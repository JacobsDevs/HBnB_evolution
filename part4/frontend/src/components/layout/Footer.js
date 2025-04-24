// This component renders the application's footer section.
// It includes navigation links, social media connections, and a newsletter signup.
// The footer is a static component that appears on all pages of the application.

import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  // Get current year for copyright notice
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      {/* Main footer content container */}
      <div className="footer-container">
        {/* Brand section with logo and social links */}
        <div className="footer-section">
          <h3>HBnB</h3>
          <p className="footer-tagline">Find your perfect place to stay</p>
          
          {/* Social media links */}
          <div className="social-links">
            {/* Note: These links currently point to localhost as placeholders */}
            <a href="localhost:3000" className="social-link" aria-label="Facebook">
              <i className="fab fa-facebook-f"></i>
            </a>
            <a href="localhost:3000" className="social-link" aria-label="Twitter">
              <i className="fab fa-twitter"></i>
            </a>
            <a href="localhost:3000" className="social-link" aria-label="Instagram">
              <i className="fab fa-instagram"></i>
            </a>
            <a href="localhost:3000" className="social-link" aria-label="LinkedIn">
              <i className="fab fa-linkedin-in"></i>
            </a>
          </div>
        </div>
        
        {/* Explore section - main site navigation */}
        <div className="footer-section">
          <h4>Explore</h4>
          <ul className="footer-links">
            <li><Link to="/places">All Places</Link></li>
            <li><Link to="/places?category=featured">Featured Places</Link></li>
            <li><Link to="/blog">Blog</Link></li>
            <li><Link to="/about">About Us</Link></li>
          </ul>
        </div>
        
        {/* Host section - for property owners */}
        <div className="footer-section">
          <h4>Host</h4>
          <ul className="footer-links">
            <li><Link to="/become-host">Become a Host</Link></li>
            <li><Link to="/host-resources">Host Resources</Link></li>
            <li><Link to="/host-login">Host Login</Link></li>
            <li><Link to="/community">Community</Link></li>
          </ul>
        </div>
        
        {/* Support section - help resources */}
        <div className="footer-section">
          <h4>Support</h4>
          <ul className="footer-links">
            <li><Link to="/help">Help Center</Link></li>
            <li><Link to="/contact">Contact Us</Link></li>
            <li><Link to="/cancel">Cancellation Options</Link></li>
            <li><Link to="/safety">Safety Information</Link></li>
          </ul>
        </div>
        
        {/* Newsletter signup section */}
        <div className="footer-section">
          <h4>Newsletter</h4>
          <p>Subscribe to receive travel inspiration and deals</p>
          <form className="newsletter-form">
            <input 
              type="email" 
              placeholder="Your email address" 
              className="newsletter-input"
              aria-label="Email for newsletter"
            />
            <button type="submit" className="newsletter-button">
              Subscribe
            </button>
          </form>
        </div>
      </div>
      
      {/* Footer bottom section with legal links and copyright */}
      <div className="footer-bottom">
        <div className="footer-bottom-content">
          <div className="footer-legal">
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/cookie">Cookie Policy</Link>
          </div>
          {/* Dynamic copyright year using JavaScript */}
          <p className="copyright">© {currentYear} HBnB. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;