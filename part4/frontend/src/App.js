// This is the main application component that sets up routing and layout.
// It defines the routes for all pages and wraps them in a consistent layout
// with Header and Footer components.

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Layout Components
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import PlaceResults from './pages/PlaceResults';
import PlaceDescription from './pages/PlaceDescription';
import ProfilePage from './pages/ProfilePage';
import AddPlace from './pages/AddPlace';

function App() {
  return (
    // Router component enables client-side routing in the application
    <Router>
      <div className="App">
        {/* Header is shown on every page */}
        <Header />
        
        {/* Main content area - this is where page components are rendered */}
        <main className="main-content">
          {/* Routes define the application's URL structure and which components to render */}
          <Routes>
            {/* Home page route - the default landing page */}
            <Route path="/" element={<Home />} />
            
            {/* Authentication routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Place listing routes */}
            <Route path="/places" element={<PlaceResults />} />
            <Route path="/places/add" element={<AddPlace />} />
            <Route path="/places/:id" element={<PlaceDescription />} />
            
            {/* User profile route - supports viewing own profile with 'me' or other users by ID */}
            <Route path="/profile/:id" element={<ProfilePage />} />
          </Routes>
        </main>
        
        {/* Footer is shown on every page */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;