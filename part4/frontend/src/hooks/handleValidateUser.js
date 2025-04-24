import { validateUser } from "../services/api";

export default async function handleValidateUser() {
  const token = localStorage.getItem('token');
  if (!token) return;
  return validateUser();
}
