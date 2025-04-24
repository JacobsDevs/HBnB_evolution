import { createBrowserRouter } from 'react-router';
import MainLayout from './components/layout/MainLayout'
import AddPlace from './pages/AddPlace';
import Home from './pages/Home';
import Login from './pages/Login';
import PlaceResults from './pages/PlaceResults';
import Register from './pages/Register';
import ProfilePage from './pages/ProfilePage'
import MyProfilePage from './pages/MyProfilePage'
import handleValidateUser from './hooks/handleValidateUser';
import handleGetPlace from './hooks/handleGetPlace';
import handleGetAmenitiesAuth from './hooks/handleGetAmenitiesAuth';
import PlaceDescription from './pages/PlaceDescription';
import { getUserProfile } from './services/api';

const router = createBrowserRouter([
  // The top component has no path.  As a result it is the Layout all
  // other routes will use.  The MainLayout component renders 
  // the Header, the Outlet, then the Footer.  The outlet is whatever child
  // accessed by the route.
  {
    Component: MainLayout, children: [
      { path: '/', Component: Home },
      { path: '/login', Component: Login },
      { path: '/register', Component: Register },
      { path: '/places', Component: PlaceResults },
      {
        path: '/places/add', Component: AddPlace, loader: async () => {
          return await handleGetAmenitiesAuth();
        }
      },
      {
        path: '/places/:placeId', Component: PlaceDescription, loader: async ({ params }) => {
          return await handleGetPlace(params.placeId)
        }
      },
      // This route has a loader to pull the required data from the backend
      // prior to the page being rendered.  By refactoring to loaders we can just
      // get what we need from the server upfront and render the page once we have it.
      {
        path: '/profile/me', Component: MyProfilePage, loader: async () => {
          // handleValidateUser is a custom hook (defined in /src/hooks)
          return await handleValidateUser();
        }
      },
      {
        path: '/profile/:userId', Component: ProfilePage, loader: async ({ params }) => {
          try {
            const user = await getUserProfile(params.userId);
            return user;
          } catch {
            return { error: '404: User Not Found' }
          }
        }
      },
      { path: '/', Component: Home },
      { path: '/', Component: Home },
      { path: '/', Component: Home },
    ]
  }
])

export default router;
