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
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/places" element={<PlaceResults />} />
            <Route path="/places/add" element={<AddPlace />} />
            <Route path="/places/:id" element={<PlaceDescription />} />
            <Route path="/profile/:id" element={<ProfilePage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;