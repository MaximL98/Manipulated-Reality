import React, { useState, useEffect, useRef } from 'react';
import PageDesign from './Styles/PageDesign.module.css';
import MainPage from './Styles/MainPage.module.css';
import { GoVideo } from "react-icons/go";
import { PiWaveformThin } from "react-icons/pi";
import { LuAmpersand } from "react-icons/lu";
import NavbarComponent from './Components/navbar.js';
import { FaCloudUploadAlt } from "react-icons/fa";
import { FaRegCheckCircle } from "react-icons/fa";
import { VscError } from "react-icons/vsc";



const ACCEPTED_FILE_TYPES = ["mp4", "mkv", "avi", "mov", "wav", "mp3", "m4a", "flac", "ogg", "aac", "wma"];

function App() {
  const [data, setData] = useState({ members: [] });
  const labelRef = useRef(null);
  const imageDivRef = useRef(null);
  const upload_span_ref = useRef(null);
  const upload_p_ref = useRef(null);
  const inputFileRef = useRef(null);
  const cloudIconRef = useRef(null);
  const CheckmarkIconRef = useRef(null);

  const [showCheckmark, setShowCheckmark] = useState(false);
  const [showError, setShowError] = useState(false);

  const handleFileUpload = (event) => {
    console.log(event.target.files[0]);
    console.log(imageDivRef);

    for (let i = 0; i < ACCEPTED_FILE_TYPES.length; i++) {
      if (event.target.files[0].name.includes(ACCEPTED_FILE_TYPES[i])) {
        console.log("Accepted file type" + event.target.files[0]);
        setShowCheckmark(true);
        setShowError(false);
        imageDivRef.current.children[1].innerText = event.target.files[0].name;
        imageDivRef.current.children[2].innerText = "File selected.";
        return;
      }
    }

    setShowError(true);
    setShowCheckmark(false);
    imageDivRef.current.children[1].innerText = "Error: Invalid file type.";
    imageDivRef.current.children[2].innerText = "Please select a valid file type.";
  }

  const fileUpload = () => {
    console.log("File uploaded!!!");
    if (inputFileRef.current) {
      upload_p_ref.current.innerText = inputFileRef.current.files[0].name;
      upload_span_ref.current.innerText = "File selected.";
    }
  }


  useEffect(() => {
    fetch("/upload")
      .then(res => res.json())
      .then(data => setData(data)); // Update entire data state
  }, []);


  return (
    <div>
      <NavbarComponent />
      <div className={PageDesign.mainDiv}>
        <h1 style={{ fontSize: "60px" }}>Manipulated Reality</h1>
        <label action='upload' method="post" encType="multipart/form-data" className={MainPage.dropArea} useRef={labelRef}>
          <input type="file" name='uploaded_file' accept="mp4,mkv,avi,mov,wav" className={MainPage.inputFile} useRef={inputFileRef} onChange={handleFileUpload} hidden />
          <div className={MainPage.uploadImageDiv} ref={imageDivRef}>
            {showCheckmark && <FaRegCheckCircle className={MainPage.uploadImage} id={MainPage.Checkmark} ref={CheckmarkIconRef} />}
            {showError && <VscError className={MainPage.uploadImage} id={MainPage.Error} ref={CheckmarkIconRef} />}
            {!showError && !showCheckmark && <FaCloudUploadAlt className={MainPage.uploadImage} ref={cloudIconRef} />}




            <p ref={upload_p_ref}>Click or drop a file here.</p>
            <span ref={upload_span_ref}>Upload a video or audio file for detection.</span>
          </div>
        </label>

        {showCheckmark && <button className={MainPage.uploadButton} onClick={fileUpload}>Upload</button>}


      <p>Below is a working upload of a video. Above is a work in progress.</p>
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
    </div>
        );
}

        export default App;