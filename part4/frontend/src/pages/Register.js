// Register.js
// This component provides a user registration form with validation.
// It handles form state, input validation, and API submission for creating new user accounts.
// After successful registration, users are redirected to the login page.

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/api';
import './Register.css';

const Register = () => {
  // Form data state with all required fields for user registration
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '' // This field is used for validation but not sent to the API
  });

  // State for handling errors and loading status
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Navigation hook for redirecting after registration
  const navigate = useNavigate();

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    // Reset error state
    setError('');

    // Client-side validation before making API call
    // Password matching validation
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      return;
    }

    // Password strength validation
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setLoading(true);

    try {
      // Remove confirm_password before sending to API
      // This is a good example of data preparation before API submission
      const { confirm_password, ...userData } = formData;

      // Call the registration API function
      console.log(userData)
      await register(userData);

      // Show success message and redirect to login page
      alert('Registration successful! Please login with your credentials.');
      navigate('/login');
    } catch (err) {
      console.error('Registration error:', err);

      // Handle different error types based on API response
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.response?.status === 400) {
        setError('Invalid registration data. Please check your information.');
      } else {
        setError('An error occurred during registration. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h2>Create Account</h2>
        {/* Display error message if there is one */}
        {error && <div className="error-message">{error}</div>}

        {/* Registration form */}
        <form onSubmit={handleSubmit}>
          {/* First Name field */}
          <div className="form-group">
            <label htmlFor="first_name">First Name</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          {/* Last Name field */}
          <div className="form-group">
            <label htmlFor="last_name">Last Name</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          {/* Email field */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          {/* Password field with requirements hint */}
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={loading}
              minLength="8"
            />
            <small className="form-text">
              Password must be at least 8 characters long and include letters, numbers, and special characters.
            </small>
          </div>

          {/* Confirm Password field */}
          <div className="form-group">
            <label htmlFor="confirm_password">Confirm Password</label>
            <input
              type="password"
              id="confirm_password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          {/* Submit button with loading state */}
          <button
            type="submit"
            className="register-button"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        {/* Link to login page for existing users */}
        <div className="login-link">
          Already have an account? <a href="/login">Login here</a>
        </div>
      </div>
    </div>
  );
};

export default Register;
