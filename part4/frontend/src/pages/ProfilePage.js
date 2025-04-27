// This component displays a user profile page with their personal information, 
// listings, and reviews. It handles both viewing your own profile and other users' profiles.
// The component fetches user data and their places from the API.

import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate, useLoaderData } from 'react-router-dom';
import { getUserProfile, getPlacesByUser } from '../services/api';
import './ProfilePage.css';
import PlaceCard from '../components/PlaceCard'

const ProfilePage = () => {
  // Extract user ID from URL parameters - could be 'me' or a specific user ID
  const { id } = useParams();
  const data = useLoaderData();

  // State variables
  const [user, setUser] = useState(null);  // User profile data
  const [places, setPlaces] = useState([]); // User's places/listings
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  const navigate = useNavigate();

  // Fetch user data and places when component mounts or ID changes
  useEffect(() => {
    try {
      if (data.error) {
        setError(data.error)
      }
      setLoading(true);
      setUser(data);
      setPlaces(data.places);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching user data:', err);
      setError('Failed to load user profile. Please try again later.');
      setLoading(false);
    }
  }, [id, navigate]); // Re-fetch when these dependencies change

  // Show loading state while data is being fetched
  if (loading) {
    return <div className="loading-container">Loading profile...</div>;
  }

  // Show error state if data couldn't be loaded
  if (error) {
    return <div className="error-container">{error}</div>;
  }

  // Show error if user not found
  if (!user) {
    return <div className="error-container">User not found</div>;
  }

  return (
    <div className="profile-page">
      {/* Profile header with user info */}
      <div className="profile-header">
        <div className="profile-picture">
          {/* Profile picture placeholder showing first initial */}
          <div className="profile-initial">{user.first_name?.charAt(0) || '?'}</div>
        </div>
        <div className="profile-info">
          <h1>{user.first_name} {user.last_name}</h1>
          <p className="profile-email">{user.email}</p>
        </div>
      </div>

      {/* Main profile content */}
      <div className="profile-content">
        {/* About section */}
        <div className="about-section">
          <h2>About Me</h2>
          {user.bio ? (
            <p>{user.bio}</p>
          ) : (
            <p className="no-data-message">
              "This user hasn't added a bio yet."
            </p>
          )}

          {/* User stats - calculated from their places data */}
          <div className="user-stats">
            <div className="stat-item">
              <span className="stat-value">{places.length}</span>
              <span className="stat-label">Places</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">
                {places.reduce((sum, place) => sum + (place.reviews?.length || 0), 0)}
              </span>
              <span className="stat-label">Reviews</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">
                {places.length > 0
                  ? new Date(Math.min(...places.map(p => new Date(p.created_at)))).getFullYear()
                  : '-'}
              </span>
              <span className="stat-label">Joined</span>
            </div>
          </div>

          {/* Admin badge - only shown to the user on their own profile */}
          {user.is_admin && (
            <div className="admin-badge">
              Administrator
            </div>
          )}
        </div>

        {/* Places section - shows listings owned by this user */}
        <div className="places-section">
          <div className="section-header">
            <h2>My Places</h2>
          </div>

          {/* Display places or a message if none exist */}
          {places.length > 0 ? (
            <div className="places-grid">
              {places.map(place => (
                  
                  <PlaceCard key={place.id} id={place.id} title={place.title} description={place.description} price={place.price} />
              
              ))}
            </div>
          ) : (
            <p className="no-data-message">
              "This user hasn't listed any places yet."
            </p>
          )}
        </div>

        {/* Reviews section - shows reviews for this user's places */}
        <div className="reviews-section">
          <h2>Reviews</h2>

          {/* Check if any places have reviews */}
          {places.some(place => place.reviews?.length > 0) ? (
            <div className="reviews-container">
              {/* Flatten reviews from all places into a single list */}
              {places.flatMap(place =>
                (place.reviews || []).map(review => (
                  <div className="review-item" key={review.id}>
                    <div className="review-header">
                      <span className="review-place">
                        For: <Link to={`/places/${place.id}`}>{place.title}</Link>
                      </span>
                      <span className="review-rating">
                        Rating: {review.rating}/5
                      </span>
                    </div>
                    <p className="review-text">{review.text}</p>
                    <div className="review-date">
                      Posted on: {new Date(review.created_at).toLocaleDateString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          ) : (
            <p className="no-data-message">
              "This user's places haven't received any reviews yet."
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
