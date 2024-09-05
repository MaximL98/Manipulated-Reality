import React, { useState, useEffect, useRef  } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import MainPage from '../Styles/MainPage.module.css';
import { GoVideo } from "react-icons/go";
import { PiWaveformThin } from "react-icons/pi";
import { LuAmpersand } from "react-icons/lu";
import NavbarComponent from './Navbar.js';
import { FaCloudUploadAlt } from "react-icons/fa";
import { FaRegCheckCircle } from "react-icons/fa";
import { VscError } from "react-icons/vsc";
import { Link, useNavigate } from 'react-router-dom';



const ACCEPTED_FILE_TYPES = ["mp4", "mkv", "avi", "mov", "wav", "mp3", "m4a", "flac", "ogg", "aac", "wma"];

function UploadFilePage() {
  const [data, setData] = useState([{}]);
  const [linkToResults, setLinkToResults] = useState(false);
  const navigate = useNavigate();



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


  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [showCheckmark, setShowCheckmark] = useState(false);
  const [showError, setShowError] = useState(false);

  // const handleFileUpload = (event) => {

  //   console.log(event.target.files[0]);
  //   console.log(imageDivRef);

  //   let filename = event.target.files[0].name;

  //   if (file && ACCEPTED_FILE_TYPES.includes(file.name.split('.').pop())) {
  //     setSelectedFile(file);
  //     setShowCheckmark(true);
  //     setShowError(false);

  //   } else {
  //     setSelectedFile(null);
  //     setShowError(true);
  //     setShowCheckmark(false);
  //     // imageDivRef.current.children[1].innerText = "Error: Invalid file type.";
  //     // imageDivRef.current.children[2].innerText = "Please select a valid file type.";
  //   }

  //   // if (ACCEPTED_FILE_TYPES.includes(filename.split('.').pop())) {
  //   //   console.log("Accepted file type " + filename);
  //   //   setShowCheckmark(true);
  //   //   setShowError(false);
  //   // imageDivRef.current.children[1].innerText = filename.slice(0, 40) + "..."; // Truncate filename
  //   // imageDivRef.current.children[2].innerText = "File selected.";

  //   // }
  //   // else {
  //   //   setShowError(true);
  //   //   setShowCheckmark(false);

  //   // }

  //   if (data['message'] === "Upload successful") {
  //     console.log("Upload successful");
  //   }
  // }

  // const fileUpload = (event) => {
  //   //console.log("File upload function called ", inputFileRef.current.files[0]);
  //   const formData = new FormData();
  //   //formData.append('uploaded_file', inputFileRef.current.files[0]);
  //   formData.append('file_type', 'video'); // Add this based on the selected option

  //   fetch('/Results', {
  //     method: 'POST',
  //     body: formData,
  //   })
  //     .then(response => response.json())
  //     .then(data => {
  //       setData(data.message || 'Upload successful');
  //       // Update UI based on the response
  //       if (data.success) {
  //         setShowCheckmark(true);
  //         setShowError(false);
  //       } else {
  //         setShowError(true);
  //         setShowCheckmark(false);
  //       }
  //     })
  //     .catch(error => {
  //       console.error('Error:', error);
  //       setData('Upload failed');
  //       setShowError(true);
  //       setShowCheckmark(false);
  //     });
  // };

  const handleFileChange = (event) => {
    const file = event.target;
    console.log(file.files[0]);

    if (file && ACCEPTED_FILE_TYPES.includes(file.name.split('.').pop())) {
      setSelectedFile(file);
      setShowCheckmark(true);
      setShowError(false);
      // Update UI with selected file info
    } else {
      setSelectedFile(null);
      setShowError(true);
      setShowCheckmark(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setShowError(true);
      setUploadStatus('Please select a valid file');
      return;
    }


    const formData = new FormData();
    formData.append('uploaded_file', selectedFile);

    const fetchResults = async () => {
      try {
        const response = await fetch('/Uploaded', {
          method: 'POST',
          body: formData // Make sure formData is properly defined
        });

        const responseData = await response.json();
        setData(responseData.message);

        setLinkToResults(true);
        navigate('/Results', {state: {videoURL: responseData[0], audioURL: responseData[1]}});

      } catch (error) {
        setData('Upload failed');
      }
    };
    fetchResults();

  };






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

  const [testComminicationData, setTestCommunicationData] = useState([{}]);

  function testClientServerCommunication(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('text_file', event.target.text_file.value); // Key-value pair

    fetch('/test', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        setTestCommunicationData(data.message);
        console.log(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  return (
    <div>
      <div className={PageDesign.mainDiv}>
        <h1 style={{ fontSize: "50px" }}>Upload a file</h1>

        <form onSubmit={testClientServerCommunication}>Example client-server communication
          <input type="text" name='text_file' />
          <button type="submit">Upload</button>
        </form>

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



        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <input type="file" name='uploaded_file' accept="mp4,mkv,avi,mov,wav,mp3" className={MainPage.inputFile} ref={inputFileRef} onChange={handleFileChange} />
          <button type="submit" className={MainPage.uploadButton}>Upload</button>
        </form>
        {uploadStatus && <p>{uploadStatus}</p>}
        {linkToResults && <Link to={`/Results?data=${data}`}>Go to results</Link>}

        <form onSubmit={handleSubmit} encType="multipart/form-data" className={MainPage.dropArea} ref={labelRef}>
          <input type="file" name='uploaded_file' className={MainPage.inputFile} ref={inputFileRef} onChange={handleFileChange} hidden />
          <div className={MainPage.uploadImageDiv} ref={imageDivRef}>
            {showCheckmark && <FaRegCheckCircle className={MainPage.uploadImage} id={MainPage.Checkmark} />}
            {showError && <VscError className={MainPage.uploadImage} id={MainPage.Error} />}
            {!showError && !showCheckmark && <FaCloudUploadAlt className={MainPage.uploadImage} />}



            <div>
              <p ref={upload_p_ref}>Click or drop a file here.</p>
            </div>
            <span ref={upload_span_ref}>Upload a video or audio file for detection.</span>

          </div>

          <button type="submit" className={MainPage.uploadButton}>Upload</button>

        </form>



      </div >
      <div>
        <h1>Register</h1>
        <form method="POST" action="/register">
          <label htmlFor="username">Username:</label>
          <input type="text" name="username" required />

          <label htmlFor="password">Password:</label>
          <input type="password" name="password" required />

          <label htmlFor="email">Email:</label>
          <input type="email" name="email" required />


          <button type="submit">Register</button>
        </form>
      </div>
      <div>
        <h1>Login</h1>
        <form method="POST" action="/loginUser">
          <label htmlFor="username">Username:</label>
          <input type="text" name="username" required />

          <label htmlFor="password">Password:</label>

          <input type="password" name="password" required />

          <button type="submit">Login</button>
        </form>
      </div>
    </div >
  );
}

export default UploadFilePage;