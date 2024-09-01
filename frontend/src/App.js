import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter, Routes } from 'react-router-dom';
import { Route } from 'react-router-dom';
import UploadFilePage from './Components/UploadFilePage.js';
import Results from './Components/Results.js';


function App() {
  const [data, setData] = useState([{}]);

  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<UploadFilePage />} />
        <Route path="/Results" element={<Results />} />
      </Routes>
    </BrowserRouter>

  );
}

export default App;