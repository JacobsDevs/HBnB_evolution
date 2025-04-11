import { createBrowserRouter } from "react-router";

// Import the components you want to map routes to
import Amenities from "./components/Amenities";
import AmenitiesNew from "./components/AmenitiesNew";
import RegisterUser from "./components/RegisterUser";
import Root from "./components/Root";

// You can also set up something called a loader that performs an operation before loading the page.
import { fetchUser, UserShow } from "./components/UserShow";

const router = createBrowserRouter([
  // Define routes like this.
  {
    path: "/",
    Component: Root,
  },
  {
    path: "/amenities",
    Component: Amenities,
  },
  {
    path: "/amenities/new",
    Component: AmenitiesNew
  },
  {
    path: "/users/register",
    Component: RegisterUser
  },
  {
    path: "/users/:userId",
    // If you want to preload data you can access the route params like this to get :userId
    // async will wait for the data to be grabbed before loading the page.
    loader: async ({ params }) => {
      let user = await fetchUser(params.userId);
      return user
    },
    Component: UserShow
  }
]);

export default router;
