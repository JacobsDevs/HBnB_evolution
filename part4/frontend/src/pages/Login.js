import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Call the login API function from our api service
      const response = await login(email, password);
      
      // Store the JWT token in localStorage
      localStorage.setItem('token', response.access_token);
      
      // Store user ID if available
      if (response.user_id) {
        localStorage.setItem('userId', response.user_id);
      }
      
      // Redirect to home page
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
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h2>Login to HBnB</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
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
          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="login-options">
        <button 
          className="create-account-btn"
          onClick={() => navigate('/register')}
          disabled={loading}
        >
          Create Account
        </button>
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