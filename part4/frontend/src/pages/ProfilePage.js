import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getUserProfile, getPlacesByUser } from '../services/api';
import './ProfilePage.css';

const ProfilePage = () => {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const isCurrentUser = id === 'me' || id === localStorage.getItem('userId');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);
        
        // Handle 'me' route
        const userId = id === 'me' ? localStorage.getItem('userId') : id;
        
        if (!userId) {
          navigate('/login?redirect=profile');
          return;
        }
        
        // Fetch user profile
        const userData = await getUserProfile(userId);
        setUser(userData);
        
        // Fetch user's places
        const placesData = await getPlacesByUser(userId);
        setPlaces(placesData || []);
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Failed to load user profile. Please try again later.');
        setLoading(false);
        
        // If unauthorized and trying to view own profile, redirect to login
        if (err.response?.status === 401 && isCurrentUser) {
          localStorage.removeItem('token');
          localStorage.removeItem('userId');
          navigate('/login?redirect=profile');
        }
      }
    };

    fetchUserData();
  }, [id, navigate, isCurrentUser]);

  if (loading) {
    return <div className="loading-container">Loading profile...</div>;
  }

  if (error) {
    return <div className="error-container">{error}</div>;
  }

  if (!user) {
    return <div className="error-container">User not found</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-picture">
          {/* Profile picture placeholder */}
          <div className="profile-initial">{user.first_name?.charAt(0) || '?'}</div>
        </div>
        <div className="profile-info">
          <h1>{user.first_name} {user.last_name}</h1>
          <p className="profile-email">{user.email}</p>
          {isCurrentUser && (
            <button className="edit-profile-btn" onClick={() => navigate('/profile/me')}>
              Edit Profile
            </button>
          )}
        </div>
      </div>
      
      <div className="profile-content">
        <div className="about-section">
          <h2>About Me</h2>
          {user.bio ? (
            <p>{user.bio}</p>
          ) : (
            <p className="no-data-message">
              {isCurrentUser 
                ? "You haven't added a bio yet. Click 'Edit Profile' to add information about yourself."
                : "This user hasn't added a bio yet."}
            </p>
          )}
          
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
          
          {isCurrentUser && user.is_admin && (
            <div className="admin-badge">
              Administrator
            </div>
          )}
        </div>
        
        <div className="places-section">
          <div className="section-header">
            <h2>My Places</h2>
            {isCurrentUser && (
              <Link to="/places/add" className="add-place-btn">
                + Add New Place
              </Link>
            )}
          </div>
          
          {places.length > 0 ? (
            <div className="places-grid">
              {places.map(place => (
                <div className="profile-place-card" key={place.id}>
                  <div className="place-image">
                    <div className="placeholder-image"></div>
                  </div>
                  <div className="place-details">
                    <h3>{place.title}</h3>
                    <p className="place-price">${place.price} / night</p>
                    <div className="place-stats">
                      <span className="stat">
                        <i className="fas fa-star"></i>
                        {place.reviews?.length > 0 
                          ? (place.reviews.reduce((sum, r) => sum + r.rating, 0) / place.reviews.length).toFixed(1)
                          : 'No ratings'}
                      </span>
                      <span className="stat">
                        <i className="fas fa-comment"></i>
                        {place.reviews?.length || 0} reviews
                      </span>
                    </div>
                    <Link to={`/places/${place.id}`} className="view-details-btn">
                      View Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data-message">
              {isCurrentUser 
                ? "You haven't listed any places yet. Click 'Add New Place' to get started!"
                : "This user hasn't listed any places yet."}
            </p>
          )}
        </div>
        
        <div className="reviews-section">
          <h2>Reviews</h2>
          
          {places.some(place => place.reviews?.length > 0) ? (
            <div className="reviews-container">
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
              {isCurrentUser 
                ? "Your places haven't received any reviews yet."
                : "This user's places haven't received any reviews yet."}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;