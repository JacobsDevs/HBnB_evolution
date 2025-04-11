// Since we used a loader in the route, we can access the return value
// of the loader with this function
import { useLoaderData } from "react-router"

// This is the function we are using in the loader of UserShow
export async function fetchUser(userId) {
  // get and return the User object from the API
  return fetch(`/api/v1/users/${userId}`)
    .then((response) => response.json())
};

export function UserShow() {
  // First we get the loader data for the page (in this case it is the User)
  const user = useLoaderData()

  // We can now access the data as you would access it off the object
  return (
    <>
      <p>{user.email}</p>
      <p>{user.first_name}</p>
    </>
  )
}
