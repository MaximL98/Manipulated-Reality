import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter, Routes } from 'react-router-dom';
import { Route } from 'react-router-dom';
import UploadFilePage from './Components/UploadFilePage.js';
import Results from './Components/Results.js';
import About from './Components/About.js';
import Contact from './Components/Contact.js';
import Navbar from './Components/Navbar.js';
import Login from './Components/Login.js';
import Register from './Components/Register.js';
import Profile from './Components/Profile.js';



function App() {
  const [data, setData] = useState([{}]);

  return (

    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<UploadFilePage />} />
        <Route path="/Results" element={<Results />} />
        <Route path="/UploadFilePage" element={<UploadFilePage />} />
        <Route path="About" element={<About />} />
        <Route path="Contact" element={<Contact />} />
        <Route path="Login" element={<Login />} />
        <Route path="Register" element={<Register />} />
        <Route path="Profile" element={<Profile />} />
      </Routes>
    </BrowserRouter>

  );
}

export default App;