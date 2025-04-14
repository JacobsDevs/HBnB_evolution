import React from 'react';
import { useParams } from 'react-router-dom';
import './ProfilePage.css';

const ProfilePage = () => {
  const { id } = useParams();

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-picture">
          {/* Profile picture will go here */}
        </div>
        <div className="profile-info">
          <h1>User Profile</h1>
          <p>Loading profile for ID: {id}</p>
        </div>
      </div>
      <div className="profile-content">
        <div className="about-section">
          <h2>About Me</h2>
          {/* About me content will go here */}
        </div>
        <div className="places-section">
          <h2>My Places</h2>
          {/* Places owned by user will go here */}
        </div>
        <div className="reviews-section">
          <h2>Reviews</h2>
          {/* Reviews for user's places will go here */}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;