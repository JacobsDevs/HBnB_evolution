import React from 'react';
import { useParams } from 'react-router-dom';
import './ProfilePage.css';
import { useNavigate} from "react-router-dom";
import { useLoaderData } from 'react-router';
import PlaceCard from '../components/PlaceCard';

const ProfilePage = () => {
  const { id } = useParams();
  const userData = useLoaderData()
  const navigate = useNavigate()

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-picture">
          {/* Profile picture will go here */}
        </div>
        <div className="profile-info">
          <h1>{userData.first_name} {userData.last_name}</h1>
          <p>{userData.email}</p>
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
          <div className='user-places container'>
            <PlaceCard></PlaceCard>
            <button type="submit" className="add-button" onClick = { () => navigate('/newplace') }
            >Add new place</button>
          </div>
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
