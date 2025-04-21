import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add authentication token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ============================== //
// =========== Places =========== //
// ============================== //
export const getAllPlaces = async (searchQuery = '') => {
  try {
    // If your API supports search parameters, you can add them here
    // const response = await api.get(`/places?search=${searchQuery}`);
    
    // If not, we'll fetch all places and filter in the component
    const response = await api.get('/places');
    return response.data;
  } catch (error) {
    console.error('Error fetching places:', error);
    throw error;
  }
};

export const getPlaceById = async (id) => {
  try {
    const response = await api.get(`/places/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching place details:', error);
    throw error;
  }
};

export const createPlace = async (placeData) => {
  try {
    const response = await api.post('/places', placeData);
    return response.data;
  } catch (error) {
    console.error('Error creating place:', error);
    throw error;
  }
};


// ============================== //
// ========== Amenities ========= //
// ============================== //
export const addAmenityToPlace = async (placeId, amenityId) => {
  try {
    const response = await api.post(`/places/${placeId}/amenities`, { amenity_id: amenityId });
    return response.data;
  } catch (error) {
    console.error('Error adding amenity to place:', error);
    throw error;
  }
};

export const getAllAmenities = async () => {
  try {
    const response = await api.get('/amenities');
    return response.data;
  } catch (error) {
    console.error('Error fetching amenities:', error);
    throw error;
  }
};

export const createAmenity = async (amenityData) => {
  try {
    const response = await api.post('/amenities', amenityData);
    return response.data;
  } catch (error) {
    console.error('Error creating amenity:', error);
    throw error;
  }
};


// ============================== //
// =========== Users ============ //
// ============================== //
export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/users', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
};

export const getUserProfile = async (id) => {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const getPlacesByUser = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}/places`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user places:', error);
    throw error;
  }
};


// Export other API services as needed
export default api;