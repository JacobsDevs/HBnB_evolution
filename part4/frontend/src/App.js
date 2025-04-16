import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { RouterProvider } from 'react-router-dom';
import './App.css';
import { router } from "./routes.js"

export default function App() {
  return (
    <RouterProvider router={router} />
  );
}
