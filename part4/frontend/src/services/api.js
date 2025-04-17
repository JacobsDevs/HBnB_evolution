import axios from 'axios';

const API_URL = 'http://localhost:5000/api/v1';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  },
});

// Add request interceptor to add authentication token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token.replace(/[""]+/g, '')}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Places services
export const getAllPlaces = async (searchQuery = '') => {
  try {
    // If your API supports search parameters, you can add them here
    // const response = await api.get(`/places?search=${searchQuery}`);

    // If not, we'll fetch all places and filter in the component
    const response = await api.get('/places/');
    return response.data;
  } catch (error) {
    console.error('Error fetching places:', error);
    throw error;
  }
};

export const getPlaceById = async (id) => {
  try {
    const response = await api.get(`/places/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching place details:', error);
    throw error;
  }
};

// Auth services
export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });
    localStorage.setItem('token', JSON.stringify(response.data.access_token))
    localStorage.setItem('user_id', JSON.stringify(response.data.user_id))
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};

// User services
export const getUserProfile = async (id) => {
  try {
    id = id.replace(/[""]+/g, '')
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const registerNewUser = async (email, password) => {
  try {
    const response = await api.post('/users', { email, password });
    return response.data;
  } catch (error) {
    console.error('Error registering new user: ', error)
    throw error;
  }
}

// Export other API services as needed
export default api;
