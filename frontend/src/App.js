import React, { useState, useEffect } from 'react';
import PageDesign from './Styles/PageDesign.module.css';
import MainPage from './Styles/MainPage.module.css';
import { GoVideo } from "react-icons/go";
import { PiWaveformThin } from "react-icons/pi";
import { LuAmpersand } from "react-icons/lu";




function App() {
  const [data, setData] = useState({ members: [] });

  useEffect(() => {
    fetch("/upload")
      .then(res => res.json())
      .then(data => setData(data)); // Update entire data state
  }, []);

  return (
    <div className={PageDesign.mainDiv}>
      <div className={PageDesign.mrLogo}>
        <div className={PageDesign.innerLogoDiv}>
          <img src="ManipulatedRealityLogo.png" alt="Manipulated Reality Logo" className={PageDesign.logoImage} />

        </div>

      </div>
      <h1>Manipulated Reality</h1>

      <div >

      </div>
      <form action='upload' method="post" encType="multipart/form-data">
        <input type="file" name='video' accept="mp4,mkv,avi" />
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