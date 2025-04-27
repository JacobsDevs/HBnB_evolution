// api.js - API service layer
// This file centralizes all API calls to the backend using Axios
// Each function corresponds to a specific API endpoint and operation

import axios from 'axios';
import { Loader } from '@googlemaps/js-api-loader'

// Base URL for the API - can be easily changed for different environments
const API_URL = 'http://localhost:8000/api/v1';

/**
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * // Basic fetch setup that would replace the axios instance below
 * const fetchAPI = async (url, options = {}) => {
 *   // Add default headers
 *   const headers = {
 *     'Content-Type': 'application/json',
 *     ...options.headers,
 *   };
 *   
 *   // Add auth token if available
 *   const token = localStorage.getItem('token');
 *   if (token) {
 *     headers['Authorization'] = `Bearer ${token}`;
 *   }
 *   
 *   // Full request options
 *   const requestOptions = {
 *     ...options,
 *     headers,
 *   };
 *   
 *   const response = await fetch(`${API_URL}${url}`, requestOptions);
 *   
 *   // Check for errors
 *   if (!response.ok) {
 *     const errorData = await response.json().catch(() => ({}));
 *     throw {
 *       status: response.status,
 *       statusText: response.statusText,
 *       data: errorData,
 *     };
 *   }
 *   
 *   // Parse JSON response
 *   return response.json();
 * };
 */

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add authentication token to requests
// This automatically adds the token to all requests without repeating code
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

/**
 * Get all places, optionally filtered by a search query
 * 
 * @param {string} searchQuery - Optional search term to filter places
 * @returns {Promise<Array>} - Array of place objects
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const getAllPlaces = async (searchQuery = '') => {
 *   try {
 *     const response = await fetchAPI(`/places`);
 *     return response;
 *   } catch (error) {
 *     console.error('Error fetching places:', error);
 *     throw error;
 *   }
 * };
 */
export const getAllPlaces = async (searchQuery = '') => {
  try {
    // If your API supports search parameters, you can add them here
    // const response = await api.get(`/places?search=${searchQuery}`);

    // If not, we'll fetch all places and filter in the component
    const response = await api.get('/places');
    return response.data; // Axios automatically parses JSON
  } catch (error) {
    console.error('Error fetching places:', error);
    throw error;
  }
};

/**
 * Get details for a specific place by ID
 * 
 * @param {string} id - The place ID
 * @returns {Promise<Object>} - Place details
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const getPlaceById = async (id) => {
 *   try {
 *     const response = await fetchAPI(`/places/${id}/`);
 *     return response;
 *   } catch (error) {
 *     console.error('Error fetching place details:', error);
 *     throw error;
 *   }
 * };
 */
export const getPlaceById = async (id) => {
  try {
    const response = await api.get(`/places/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching place details:', error);
    throw error;
  }
};

/**
 * Create a new place listing
 * 
 * @param {Object} placeData - Place data including title, description, price, etc.
 * @returns {Promise<Object>} - The created place
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const createPlace = async (placeData) => {
 *   try {
 *     const response = await fetchAPI('/places', {
 *       method: 'POST',
 *       body: JSON.stringify(placeData)
 *     });
 *     return response;
 *   } catch (error) {
 *     console.error('Error creating place:', error);
 *     throw error;
 *   }
 * };
 */
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

/**
 * Add an amenity to a place
 * 
 * @param {string} placeId - The place ID
 * @param {string} amenityId - The amenity ID to add
 * @returns {Promise<Object>} - Result of the operation
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const addAmenityToPlace = async (placeId, amenityId) => {
 *   try {
 *     const response = await fetchAPI(`/places/${placeId}/amenities`, {
 *       method: 'POST',
 *       body: JSON.stringify({ amenity_id: amenityId })
 *     });
 *     return response;
 *   } catch (error) {
 *     console.error('Error adding amenity to place:', error);
 *     throw error;
 *   }
 * };
 */
export const addAmenityToPlace = async (placeId, amenityId) => {
  try {
    const response = await api.post(`/places/${placeId}/amenities`, { amenity_id: amenityId });
    return response.data;
  } catch (error) {
    console.error('Error adding amenity to place:', error);
    throw error;
  }
};

/**
 * Get all available amenities
 * 
 * @returns {Promise<Array>} - Array of amenity objects
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const getAllAmenities = async () => {
 *   try {
 *     const response = await fetchAPI('/amenities');
 *     return response;
 *   } catch (error) {
 *     console.error('Error fetching amenities:', error);
 *     throw error;
 *   }
 * };
 */
export const getAllAmenities = async () => {
  try {
    const response = await api.get('/amenities');
    return response.data;
  } catch (error) {
    console.error('Error fetching amenities:', error);
    throw error;
  }
};

/**
 * Create a new amenity
 * 
 * @param {Object} amenityData - Amenity data including name and description
 * @returns {Promise<Object>} - The created amenity
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const createAmenity = async (amenityData) => {
 *   try {
 *     const response = await fetchAPI('/amenities', {
 *       method: 'POST',
 *       body: JSON.stringify(amenityData)
 *     });
 *     return response;
 *   } catch (error) {
 *     console.error('Error creating amenity:', error);
 *     throw error;
 *   }
 * };
 */
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

/**
 * User login
 * 
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @returns {Promise<Object>} - Login response with token and user ID
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const login = async (email, password) => {
 *   try {
 *     const response = await fetchAPI('/auth/login', {
 *       method: 'POST',
 *       body: JSON.stringify({ email, password })
 *     });
 *     return response;
 *   } catch (error) {
 *     console.error('Error logging in:', error);
 *     throw error;
 *   }
 * };
 */
export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};

/**
 * Register a new user
 * 
 * @param {Object} userData - User data including first_name, last_name, email, password
 * @returns {Promise<Object>} - The created user
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const register = async (userData) => {
 *   try {
 *     const response = await fetchAPI('/users', {
 *       method: 'POST',
 *       body: JSON.stringify(userData)
 *     });
 *     return response;
 *   } catch (error) {
 *     console.error('Error registering user:', error);
 *     throw error;
 *   }
 * };
 */
export const register = async (userData) => {
  try {
    const response = await api.post('/users/', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
};

/**
 * Get a user's profile by ID
 * 
 * @param {string} id - User ID
 * @returns {Promise<Object>} - User profile data
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const getUserProfile = async (id) => {
 *   try {
 *     const response = await fetchAPI(`/users/${id}`);
 *     return response;
 *   } catch (error) {
 *     console.error('Error fetching user profile:', error);
 *     throw error;
 *   }
 * };
 */
export const getUserProfile = async (id) => {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

/**
 * Get all places owned by a specific user
 * 
 * @param {string} userId - User ID
 * @returns {Promise<Array>} - Array of place objects
 * 
 * FETCH EQUIVALENT:
 * ----------------
 * export const getPlacesByUser = async (userId) => {
 *   try {
 *     const response = await fetchAPI(`/users/${userId}/places`);
 *     return response;
 *   } catch (error) {
 *     console.error('Error fetching user places:', error);
 *     throw error;
 *   }
 * };
 */
export const getPlacesByUser = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}/places`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user places:', error);
    throw error;
  }
};


export const validateUser = async () => {
  try {
    const response = await api.get('/users/me');
    return response.data;
  } catch (error) {
    console.error('Error validating user: ', error);
    throw error;
  };
};


// ============================== //
// =========== Reviews ========== //
// ============================== //

/**
 * Get reviews for a specific place
 * 
 * @param {string} placeId - The place ID
 * @returns {Promise<Array>} - Array of review objects
 */
export const getReviewsByPlace = async (placeId) => {
  try {
    const response = await api.get(`/places/${placeId}/reviews`);
    return response.data;
  } catch (error) {
    console.error('Error fetching reviews for place:', error);
    throw error;
  }
};

/**
 * Create a new review for a place
 * 
 * @param {Object} reviewData - Review data including text, rating, and place_id
 * @returns {Promise<Object>} - The created review
 */
export const createReview = async (reviewData) => {
  try {
    const response = await api.post('/reviews', reviewData);
    return response.data;
  } catch (error) {
    console.error('Error creating review:', error);
    throw error;
  }
};

/**
 * Update an existing review
 * 
 * @param {string} reviewId - The review ID
 * @param {Object} reviewData - Updated review data
 * @returns {Promise<Object>} - The updated review
 */
export const updateReview = async (reviewId, reviewData) => {
  try {
    const response = await api.put(`/reviews/${reviewId}`, reviewData);
    return response.data;
  } catch (error) {
    console.error('Error updating review:', error);
    throw error;
  }
};

/**
 * Delete a review
 * 
 * @param {string} reviewId - The review ID
 * @returns {Promise<Object>} - Response from the API
 */
export const deleteReview = async (reviewId) => {
  try {
    const response = await api.delete(`/reviews/${reviewId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting review:', error);
    throw error;
  }
};

// Export the axios instance for use in other modules if needed
export default api;
