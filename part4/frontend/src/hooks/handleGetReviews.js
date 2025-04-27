import { getReviewsByPlace } from "../services/api";

export default async function handleGetReviews(placeId) {
  if (!placeId) return [];
  
  try {
    const reviews = await getReviewsByPlace(placeId);
    return reviews;
  } catch (error) {
    console.error('Error fetching reviews:', error);
    return { error: 'Failed to load reviews' };
  }
}