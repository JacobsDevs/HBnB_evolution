import { createBrowserRouter } from "react-router";
import MainLayout from "./components/layout/MainLayout.js";
import Home from './pages/Home'
import Login from './pages/Login'
import RegisterUser from './pages/RegisterUser'
import PlaceResults from './pages/PlaceResults'
import PlaceDescription from './pages/PlaceDescription.js'
import ProfilePage from './pages/ProfilePage.js'
import { getUserProfile } from "./services/api.js";


export const router = createBrowserRouter([
  {
    Component: MainLayout, children: [
      { path: "/", Component: Home },
      { path: "/login", Component: Login },
      { path: "/register", Component: RegisterUser },
      {
        path: "/profile/me", loader: () => {
          return getUserProfile(localStorage.getItem('user_id'))
        }, Component: ProfilePage
      },
      { path: "/places", Component: PlaceResults },
      { path: "/places/:placeid", Component: PlaceDescription },
    ]
  }
])

