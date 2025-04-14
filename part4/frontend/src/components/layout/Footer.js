import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>HBnB</h3>
          <p className="footer-tagline">Find your perfect place to stay</p>
          <div className="social-links">
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
        
        <div className="footer-section">
          <h4>Explore</h4>
          <ul className="footer-links">
            <li><Link to="/places">All Places</Link></li>
            <li><Link to="/places?category=featured">Featured Places</Link></li>
            <li><Link to="/blog">Blog</Link></li>
            <li><Link to="/about">About Us</Link></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Host</h4>
          <ul className="footer-links">
            <li><Link to="/become-host">Become a Host</Link></li>
            <li><Link to="/host-resources">Host Resources</Link></li>
            <li><Link to="/host-login">Host Login</Link></li>
            <li><Link to="/community">Community</Link></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Support</h4>
          <ul className="footer-links">
            <li><Link to="/help">Help Center</Link></li>
            <li><Link to="/contact">Contact Us</Link></li>
            <li><Link to="/cancel">Cancellation Options</Link></li>
            <li><Link to="/safety">Safety Information</Link></li>
          </ul>
        </div>
        
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
      
      <div className="footer-bottom">
        <div className="footer-bottom-content">
          <div className="footer-legal">
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/cookie">Cookie Policy</Link>
          </div>
          <p className="copyright">© {currentYear} HBnB. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;