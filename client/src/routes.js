import { createBrowserRouter } from "react-router";
import Amenities from "./components/Amenities";
import AmenitiesNew from "./components/AmenitiesNew";
import RegisterUser from "./components/RegisterUser";
import Root from "./components/Root";

const router = createBrowserRouter([
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
  }
]);

export default router;
