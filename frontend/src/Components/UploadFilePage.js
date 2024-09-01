import React, { useState, useEffect, useRef } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import MainPage from '../Styles/MainPage.module.css';
import { GoVideo } from "react-icons/go";
import { PiWaveformThin } from "react-icons/pi";
import { LuAmpersand } from "react-icons/lu";
import NavbarComponent from './Navbar.js';
import { FaCloudUploadAlt } from "react-icons/fa";
import { FaRegCheckCircle } from "react-icons/fa";
import { VscError } from "react-icons/vsc";
import { Link } from 'react-router-dom';

const ACCEPTED_FILE_TYPES = ["mp4", "mkv", "avi", "mov", "wav", "mp3", "m4a", "flac", "ogg", "aac", "wma"];

function UploadFilePage() {

  let currentButton = "videoAudio";
  const labelRef = useRef(null);
  const imageDivRef = useRef(null);
  const upload_span_ref = useRef(null);
  const upload_p_ref = useRef(null);
  const inputFileRef = useRef(null);
  const cloudIconRef = useRef(null);
  const CheckmarkIconRef = useRef(null);
  const videoAudioButtonRef = useRef(null);
  const videoButtonRef = useRef(null);
  const audioButtonRef = useRef(null);
  const iconChoiceDivVideoAudioRef = useRef(null);
  const iconChoiceDivVideoRef = useRef(null);
  const iconChoiceDivAudioRef = useRef(null);


  const [showCheckmark, setShowCheckmark] = useState(false);
  const [showError, setShowError] = useState(false);

  const handleFileUpload = (event) => {
    console.log(event.target.files[0]);
    console.log(imageDivRef);

    let filename = event.target.files[0].name;

    if (ACCEPTED_FILE_TYPES.includes(filename.split('.').pop())) {
      console.log("Accepted file type " + filename);
      setShowCheckmark(true);
      setShowError(false);
      imageDivRef.current.children[1].innerText = filename.slice(0, 40) + "..."; // Truncate filename
      imageDivRef.current.children[2].innerText = "File selected.";
    }
    else {
      setShowError(true);
      setShowCheckmark(false);
      imageDivRef.current.children[1].innerText = "Error: Invalid file type.";
      imageDivRef.current.children[2].innerText = "Please select a valid file type.";
    }
  }

  const fileUpload = () => {
    console.log("File uploaded!!!");
    if (inputFileRef.current) {
      upload_p_ref.current.innerText = inputFileRef.current.files[0].name;
      upload_span_ref.current.innerText = "File selected.";
    }
  }





  function buttonClicked(type) {
    switch (type) {
      case "videoAudio":
        videoAudioButtonRef.current.className = MainPage.ChoiceButtonActive;
        videoButtonRef.current.className = MainPage.ChoiceButton;
        audioButtonRef.current.className = MainPage.ChoiceButton;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #000000";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #ffffff";
        break;
      case "video":
        videoAudioButtonRef.current.className = MainPage.ChoiceButton;
        videoButtonRef.current.className = MainPage.ChoiceButtonActive;
        audioButtonRef.current.className = MainPage.ChoiceButton;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #000000";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #ffffff";
        break;
      case "audio":
        videoAudioButtonRef.current.className = MainPage.ChoiceButton;
        videoButtonRef.current.className = MainPage.ChoiceButton;
        audioButtonRef.current.className = MainPage.ChoiceButtonActive;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #000000";
        break;
      default:
        console.log("Invalid button");
    }
  }

  return (
    <div>
      <NavbarComponent />
      <div className={PageDesign.mainDiv}>
        <h1 style={{ fontSize: "50px" }}>Upload a file</h1>
        <p>Upload a video or audio file for detection. Supported video formats: mp4, mvk, avi, mov. supported audio formats: wav, mp3. </p>

        <div className={MainPage.DetectionTypeChoiceDiv}>

          <div ref={videoAudioButtonRef} className={MainPage.ChoiceButton} onClick={(event) => { buttonClicked("videoAudio"); event.stopPropagation(); }}>
            <div style={{ display: "flex", justifyContent: "center", flexDirection: "column", marginRight: "20px" }}>
              <h2 style={{ margin: 0, padding: 0 }}>Video</h2>
              <h2 style={{ margin: 0, padding: 0 }}>&</h2>
              <h2 style={{ margin: 0, padding: 0 }}>Audio</h2>
            </div>
            <div ref={iconChoiceDivVideoAudioRef} style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderLeft: "2px solid #ffffff", height: "80px", justifyContent: "center", paddingLeft: "30px" }}>
              <GoVideo style={{ height: "40px", width: "40px" }} />
              <LuAmpersand style={{ height: "25px", width: "25px" }} />
              <PiWaveformThin style={{ height: "40px", width: "40px" }} />
            </div>

          </div>
          <div ref={videoButtonRef} className={MainPage.ChoiceButton} onClick={(event) => { buttonClicked("video"); event.stopPropagation(); }}>
            <h2 style={{ display: "flex", justifyContent: "center", flexDirection: "column", marginRight: "20px" }}>Video</h2>

            <div ref={iconChoiceDivVideoRef} style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderLeft: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingLeft: "30px" }}>
              <GoVideo style={{ height: "40px", width: "40px" }} />

            </div>
          </div>
          <div ref={audioButtonRef} className={MainPage.ChoiceButton} onClick={(event) => { buttonClicked("audio"); event.stopPropagation(); }}>
            <h2 style={{ display: "flex", justifyContent: "center", flexDirection: "column", marginRight: "20px" }}>Audio</h2>

            <div ref={iconChoiceDivAudioRef} style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderLeft: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingLeft: "30px" }}>
              <PiWaveformThin style={{ height: "40px", width: "40px" }} />

            </div>
          </div>

        </div>

        <form action='/api/upload' method="post" encType="multipart/form-data">
          <input type="file" name='uploaded_file' accept="mp4,mkv,avi,mov" className={MainPage.inputFile} useRef={inputFileRef} onChange={handleFileUpload} />
          <button className={MainPage.uploadButton} onClick={fileUpload()}>Upload</button>
        </form>
        <form action='upload' method="post" encType="multipart/form-data" className={MainPage.dropArea} useRef={labelRef}>
          <input type="file" name='uploaded_file' className={MainPage.inputFile} useRef={inputFileRef} onChange={handleFileUpload} hidden />
          <div className={MainPage.uploadImageDiv} ref={imageDivRef}>
            {showCheckmark && <FaRegCheckCircle className={MainPage.uploadImage} id={MainPage.Checkmark} ref={CheckmarkIconRef} />}
            {showError && <VscError className={MainPage.uploadImage} id={MainPage.Error} ref={CheckmarkIconRef} />}
            {!showError && !showCheckmark && <FaCloudUploadAlt className={MainPage.uploadImage} ref={cloudIconRef} />}



            <div>
              <p ref={upload_p_ref}>Click or drop a file here.</p>
            </div>
            <span ref={upload_span_ref}>Upload a video or audio file for detection.</span>

          </div>

          {showCheckmark && <Link to="/Components/Results.js"> <button className={MainPage.uploadButton} onClick={fileUpload()}>Upload</button></Link>}

        </form>



      </div >
      <div>
        <h1>Register</h1>
        <form method="POST" action="/register">
          <label for="username">Username:</label>
          <input type="text" name="username" required />

          <label for="password">Password:</label>
          <input type="password" name="password" required />

          <label for="email">Email:</label>
          <input type="email" name="email" required />


          <button type="submit">Register</button>
        </form>
      </div>
      <div>
        <h1>Login</h1>
        <form method="POST" action="/loginUser">
          <label for="username">Username:</label>
          <input type="text" name="username" required />

          <label for="password">Password:</label>

          <input type="password" name="password" required />

          <button type="submit">Login</button>
        </form>
      </div>
    </div >
  );
}

export default UploadFilePage;