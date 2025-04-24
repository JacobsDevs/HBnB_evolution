import { getPlaceById } from "../services/api";

export default async function handleGetPlace(placeId) {
  if (!placeId) return;
  return getPlaceById(placeId)
}
