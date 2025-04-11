import React from 'react';
import ReactDOM from 'react-dom/client';
import Amenities from './components/Amenities';
import Root from './components/Root'
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from 'react-router';
import router from './routes'

const root = document.getElementById("root")

ReactDOM.createRoot(root).render(
  <RouterProvider router={router} />
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
