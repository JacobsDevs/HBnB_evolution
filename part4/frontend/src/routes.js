import { createBrowserRouter } from "react-router";
import MainLayout from "./components/layout/MainLayout.js";
import Home from './pages/Home'
import PlaceResults from './pages/PlaceResults'
import Login from './pages/Login'
import PlaceDescription from './pages/PlaceDescription'
import ProfilePage from './pages/ProfilePage'
import RegisterUser from './pages/RegisterUser'


export const router = createBrowserRouter([
  {
    Component: MainLayout, children: [
      { path: "/", Component: Home },
      { path: "/places", Component: PlaceResults },
      { path: "/login", Component: Login },
      { path: "/register", Component: RegisterUser },
      { path: "/places/:placeid", Component: PlaceDescription },
      { path: "/profile/:userid", Component: ProfilePage }
    ]
  }
])

