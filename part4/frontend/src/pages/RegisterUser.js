import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
import './Login.css';
import registerNewUser, { getPlaceById, login } from '../services/api'

export default function RegisterUser() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  // const navigate = useNavigate();

  async function register() {
    let request = new Request("http://localhost:5000/api/v1/users/",
      {
        headers: { "Content-Type": "application/json" },
        method: "post",
        body: `{"first_name": "${firstName}", "last_name": "${lastName}", "email": "${email}", "password": "${password}"}`
      })
    let data = await fetch(request).then(
      (response) => response.json())
    if (data.id) {
      const res = await login(email, password);
    }
  }


  return (
    <div className="login-page">
      <div className="login-container">
        <h2>Register new User</h2>
        {error && <div className="error-message">{error}</div>}
        <form action={register}>
          <div className="form-group">
            <label htmlFor="firstName">First Name</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="lastName">Last Name</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="login-button">Register</button>
        </form>
        <div className="login-options">
          <button className="create-account-btn">Create Account</button>
          <button className="forgot-password-btn">Forgot Password?</button>
        </div>
      </div>
    </div>
  );
};
