import { getAllAmenities, getPlaceById } from "../services/api";

export default async function handleGetAmenitiesAuth() {
  if (!localStorage.getItem('token')) return;
  try {
    return await getAllAmenities();
  } catch {
    return { error: 'Request Failed' }
  }
}
