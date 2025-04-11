import { createBrowserRouter } from "react-router";
import Amenities from "./components/Amenities.js"
import AmenitiesSearch from "./components/AmenitiesSearch.js"
import Root from "./components/Root.js"

const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
  },
  {
    path: "/amenities",
    Component: Amenities
  },
  {
    path: "/amenities/search",
    Component: AmenitiesSearch
  }
]);

export default router;
