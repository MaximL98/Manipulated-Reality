import React, { useState, useEffect } from 'react';
import PageDesign from './Styles/PageDesign.module.css';
import MainPage from './Styles/MainPage.module.css';
import Navbar from './Styles/Navbar.module.css';
import { GoVideo } from "react-icons/go";
import { PiWaveformThin } from "react-icons/pi";
import { LuAmpersand } from "react-icons/lu";
import NavbarComponent from './Components/navbar.js';
import { FaCloudUploadAlt } from "react-icons/fa";





function App() {
  const [data, setData] = useState({ members: [] });

  useEffect(() => {
    fetch("/upload")
      .then(res => res.json())
      .then(data => setData(data)); // Update entire data state
  }, []);

  return (
    <div className={PageDesign.mainDiv}>
      <NavbarComponent />

      <h1>Manipulated Reality</h1>
      <form action='upload' method="post" encType="multipart/form-data">
        <input type="file" name='video' accept="mp4,mkv,avi" />
        <button>Upload</button>
      </form>

      <form action='upload' method="post" encType="multipart/form-data" className={MainPage.dropArea}>
        <input type="file" name='video' accept="mp4,mkv,avi,mov,wav" className={MainPage.inputFile}/>
        <div className={MainPage.uploadImageDiv}>
          <FaCloudUploadAlt className={MainPage.uploadImage}/>
          <p>Click or drop a file here.</p>
          <span>Upload a video or audio file for detection.</span>
        </div>
        <button>Upload</button>
      </form>


      <div className={MainPage.DetectionTypeChoiceDiv}>
        <div className={MainPage.ChoiceButton}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderRight: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingRight: "30px" }}>
            <GoVideo style={{ height: "40px", width: "40px" }} />
            <LuAmpersand style={{ height: "25px", width: "25px" }} />
            <PiWaveformThin style={{ height: "40px", width: "40px" }} />
          </div>
          <h2>Video & Audio</h2>
        </div>
        <div className={MainPage.ChoiceButton}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderRight: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingRight: "30px" }}>
            <GoVideo style={{ height: "40px", width: "40px" }} />

          </div>
          <h2>Video Only</h2>
        </div>
        <div className={MainPage.ChoiceButton}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderRight: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingRight: "30px" }}>
            <PiWaveformThin style={{ height: "40px", width: "40px" }} />

          </div>
          <h2>Audio Only</h2>
        </div>

      </div>
    </div>

  );
}

export default App;