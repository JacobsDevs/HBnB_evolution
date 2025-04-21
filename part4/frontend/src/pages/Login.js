// This component handles user authentication through a login form.
// It manages form state, submits login credentials to the API,
// and handles the auth token that's returned upon successful login.

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import './Login.css';

const Login = () => {
  // State for form inputs
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // State for error handling and loading
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Navigation hook for redirecting after login
  const navigate = useNavigate();

  // Form submission handler
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent default form submission behavior
    setError('');  // Clear any previous errors
    setLoading(true);  // Set loading state to show processing

    try {
      // Call the login API function from our api service
      // This is where we use the Axios implementation to make an HTTP request
      const response = await login(email, password);
      
      // On successful login, store the JWT token in localStorage
      // This token will be used for authentication in subsequent API requests
      localStorage.setItem('token', response.access_token);
      
      // Store user ID if available
      if (response.user_id) {
        localStorage.setItem('userId', response.user_id);
      }
      
      // Redirect to home page after successful login
      navigate('/');
    } catch (err) {
      console.error('Login error:', err);
      
      // Set appropriate error message based on response
      if (err.response?.status === 401) {
        setError('Invalid email or password');
      } else {
        setError('An error occurred during login. Please try again.');
      }
    } finally {
      setLoading(false);  // Turn off loading state
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h2>Login to HBnB</h2>
        {/* Display error message if there is one */}
        {error && <div className="error-message">{error}</div>}
        
        {/* Login form */}
        <form onSubmit={handleSubmit}>
          {/* Email input field */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          
          {/* Password input field */}
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          
          {/* Submit button with loading state */}
          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        {/* Additional options */}
        <div className="login-options">
          {/* Registration link */}
          <button 
            className="create-account-btn"
            onClick={() => navigate('/register')}
            disabled={loading}
          >
            Create Account
          </button>
          
          {/* Password recovery link */}
          <button 
            className="forgot-password-btn"
            onClick={() => navigate('/forgot-password')}
            disabled={loading}
          >
            Forgot Password?
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;