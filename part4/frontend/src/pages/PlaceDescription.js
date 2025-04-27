import React, { useState, useEffect } from 'react';
import { useParams, Link, useLoaderData, useNavigate } from 'react-router-dom';
import PlaceMap from '../components/PlaceMap';
import ReviewForm from '../components/ReviewForm';
import ReviewItem from '../components/ReviewItem';
import { getPlaceById, getUserProfile } from '../services/api';
import './PlaceDescription.css';

const PlaceDescription = () => {
  // Get the component data from the loader
  const data = useLoaderData();
  const navigate = useNavigate();

  // State variables
  const [place, setPlace] = useState(null);  // The place data
  const [owner, setOwner] = useState(null);  // Place owner information
  const [reviewers, setReviewers] = useState({});  // Map of user IDs to reviewer information
  const [loading, setLoading] = useState(true);  // Loading state
  const [error, setError] = useState(null);  // Error state
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Auth state
  const [currentUserId, setCurrentUserId] = useState(null); // Current user ID
  const [reviewToEdit, setReviewToEdit] = useState(null); // Review being edited

  // Fetch place details and reviewer information when component mounts or data changes
  useEffect(() => {
    const fetchPlaceData = async () => {
      setLoading(true);
      
      // Check if user is authenticated and get user ID
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');
      setIsAuthenticated(!!token);
      setCurrentUserId(userId || null);
  
      setPlace(data);
      setOwner(data.owner);
      
      // If the place has reviews, fetch reviewer information for each unique reviewer
      if (data.reviews && data.reviews.length > 0) {
        try {
          // Get unique reviewer IDs to avoid duplicate API calls
          const uniqueReviewerIds = [...new Set(data.reviews.map(review => review.user_id))];
          const reviewersData = {};
  
          // Use Promise.all to fetch all reviewer data in parallel
          await Promise.all(uniqueReviewerIds.map(async (userId) => {
            try {
              const userData = await getUserProfile(userId);
              reviewersData[userId] = userData;
            } catch (reviewerError) {
              console.error(`Error fetching reviewer ${userId} details:`, reviewerError);
              // Not a critical error - we can display reviews without reviewer details if needed
            }
          }));
  
          setReviewers(reviewersData);
        } catch (error) {
          console.error('Error fetching reviewer details:', error);
          // This error shouldn't prevent the component from rendering
        }
      }
  
      setLoading(false);
    };

    fetchPlaceData();
  }, [data]); // Re-run when place data changes

  // Handle after a new review is added
  const handleReviewAdded = async (newReview) => {
    try {
      // Fetch updated place data to get the new review included
      const placeId = place.id;
      const updatedPlaceData = await getPlaceById(placeId);
      setPlace(updatedPlaceData);
      
      // Fetch reviewer information for the new review
      if (newReview.user_id && !reviewers[newReview.user_id]) {
        try {
          const userData = await getUserProfile(newReview.user_id);
          setReviewers(prevReviewers => ({
            ...prevReviewers,
            [newReview.user_id]: userData
          }));
        } catch (error) {
          console.error(`Error fetching new reviewer ${newReview.user_id} details:`, error);
        }
      }
    } catch (err) {
      console.error('Error refreshing place data after review:', err);
    }
  };

  // Handle after a review is updated
  const handleReviewUpdated = async (updatedReview) => {
    // If updatedReview is null, it means edit was canceled
    if (updatedReview === null) {
      setReviewToEdit(null);
      return;
    }
    
    try {
      // Fetch updated place data
      const placeId = place.id;
      const updatedPlaceData = await getPlaceById(placeId);
      setPlace(updatedPlaceData);
      
      // Clear the edit state
      setReviewToEdit(null);
    } catch (err) {
      console.error('Error refreshing place data after review update:', err);
    }
  };

  // Handle when a review is deleted
  const handleReviewDeleted = async (deletedReviewId) => {
    try {
      // Fetch updated place data
      const placeId = place.id;
      const updatedPlaceData = await getPlaceById(placeId);
      setPlace(updatedPlaceData);
    } catch (err) {
      console.error('Error refreshing place data after review deletion:', err);
    }
  };

  // Handle edit button click for a review
  const handleEditClick = (review) => {
    setReviewToEdit(review);
    
    // Scroll to the review form for better UX
    setTimeout(() => {
      const reviewFormElement = document.querySelector('.review-form-container.edit-mode');
      if (reviewFormElement) {
        reviewFormElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  };

  // Show loading state while data is being fetched
  if (loading) {
    return <div className="loading-container">Loading place details...</div>;
  }

  // Show error state if place data couldn't be loaded
  if (error) {
    return <div className="error-container">{error}</div>;
  }

  // Show error if place not found
  if (!place) {
    return <div className="error-container">Place not found</div>;
  }

  // Main component rendering with place data
  return (
    <div className="place-description-page">
      <h1>{place.title}</h1>

      {/* Image gallery - currently a placeholder */}
      <div className="place-gallery">
        <div className="placeholder-gallery">
          <p>No photos available</p>
        </div>
      </div>

      {/* Main content area with place info and booking panel */}
      <div className="place-content">
        {/* Left column - Place information */}
        <div className="place-info">
          <h2>Description</h2>
          <p>{place.description}</p>

          <div className="location-info">
            <h3>Location</h3>
            <PlaceMap lat={place.latitude} long={place.longitude} />
          </div>
        </div>

        {/* Right column - Booking information */}
        <div className="reservation-panel">
          <h2>Booking Information</h2>
          <div className="price-section">
            <span className="price-amount">${place.price}</span> per night
          </div>
          <button className="book-now-btn">Book Now</button>

          <div className="reservation-details">
            <p>Contact the host for availability.</p>
            <p>Check-in time: 3:00 PM</p>
            <p>Check-out time: 11:00 AM</p>
          </div>
        </div>
      </div>

      {/* Amenities section */}
      <div className="amenities-section">
        <h2>Amenities</h2>
        {/* Conditional rendering based on whether amenities exist */}
        {place.amenities && place.amenities.length > 0 ? (
          <div className="amenities-list">
            {place.amenities.map(amenity => (
              <div className="amenity-item" key={amenity.id}>
                <i className="fas fa-check"></i> {amenity.name}
                {amenity.description && <p className="amenity-description">{amenity.description}</p>}
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data-message">No amenities listed for this place.</p>
        )}
      </div>

      {/* Reviews section */}
      <div className="reviews-section">
        <h2>Reviews</h2>
        {place.reviews && place.reviews.length > 0 ? (
          <div className="reviews-list">
            {/* Map through reviews and display with reviewer information if available */}
            {place.reviews.map(review => {
              // Try to get reviewer information, fallback to "Anonymous" if not available
              const reviewer = reviewers[review.user_id];
              const reviewerName = reviewer
                ? `${reviewer.first_name} ${reviewer.last_name}`
                : 'Anonymous User';

              return (
                <ReviewItem
                  key={review.id}
                  review={review}
                  reviewerName={reviewerName}
                  currentUserId={currentUserId}
                  onEditClick={handleEditClick}
                  onReviewDeleted={handleReviewDeleted}
                />
              );
            })}
          </div>
        ) : (
          <p className="no-data-message">No reviews yet. Be the first to leave a review!</p>
        )}
        
        {/* Only show the review form if not in edit mode */}
        {!reviewToEdit && (
          <ReviewForm 
            placeId={place.id} 
            onReviewAdded={handleReviewAdded}
          />
        )}
        
        {/* Show edit form if a review is being edited */}
        {reviewToEdit && (
          <ReviewForm 
            placeId={place.id}
            reviewToEdit={reviewToEdit}
            onReviewUpdated={handleReviewUpdated}
          />
        )}
      </div>

      {/* Host profile section */}
      <div className="owner-profile">
        <h2>Meet the Host</h2>
        {place.owner_id ? (
          <div className="host-info">
            <div className="host-placeholder-image"></div>
            <div className="host-details">
              {/* Display owner information if available */}
              {owner ? (
                <>
                  <h3>{owner.first_name} {owner.last_name}</h3>
                  {owner.email && (
                    <p className="host-email">Contact: {owner.email}</p>
                  )}
                </>
              ) : (
                <p>Host ID: {place.owner_id}</p>
              )}
              <Link to={`/profile/${place.owner_id}`} className="view-profile-btn">
                View Host Profile
              </Link>
            </div>
          </div>
        ) : (
          <p className="no-data-message">Host information unavailable.</p>
        )}
      </div>
    </div>
  );
};

export default PlaceDescription;
