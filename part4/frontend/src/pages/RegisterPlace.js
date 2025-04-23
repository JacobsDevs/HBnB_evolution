import React, {useState} from 'react';
import { useNavigate} from "react-router-dom";
import { registerNewPlace } from '../services/api';
import "./RegisterPlace.css"



export default function RegisterPlace() {
    const [title, setTitle] = useState()
    const [description, setDescription] = useState()
    const [price, setPrice] = useState()
    const [latitude, setLatitude] = useState()
    const [longitude, setLongitude] = useState()
    const [amenities, setAmenities] = useState([])
    const navigate = useNavigate()

    async function newPlace (e) {
      e.preventDefault();

      const placeData = { 
        title,
        description,
        price: parseFloat(price),
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        amenities: amenities.split(',').map(a => a.trim()),
        // owner_id: localStorage.getItem('user_id')
      }
      
      try {
        await registerNewPlace(placeData);
        navigate('/profile/me')
      } catch (err) {
        console.error(err)
      };
    }
    
  return (
  <div className="newplace">
      <div className="newplace-container">
        <h2>Place Registration</h2>
        <form onSubmit={newPlace}>
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <input
              type="text"
              id="description"
              name="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Price</label>
            <input
              type="number"
              id="price"
              name="price"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="latitude">Latitude</label>
            <input
              type="number"
              id="latitude"
              name="latitude"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="longitude">Longitude</label>
            <input
              type="number"
              id="longitude"
              name="longitude"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="amenities">Amenities</label>
            <input
              type="text"
              id="amenities"
              name="amenities"
              value={amenities}
              onChange={(e) => setAmenities(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="newplace-button" >Register</button>
        </form>
      </div>
    </div>
  )
}
