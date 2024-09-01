import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter, Routes } from 'react-router-dom';
import { Route } from 'react-router-dom';
import UploadFilePage from './Components/UploadFilePage';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/UploadFilePage" element={<UploadFilePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;