import React, { useState, useEffect, useRef, useCallback } from 'react';
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
import { useDropzone } from 'react-dropzone';
import { MdOutlineFileDownload } from "react-icons/md";
import ReactPlayer from 'react-player';
import { AuthContext } from './AuthProvider';
import { useContext } from 'react';




const ACCEPTED_VIDEO_TYPES = ["mp4", "mkv", "avi", "mov"];
const ACCEPTED_AUDIO_TYPES = ["wav", "mp3", "m4a", "flac", "ogg", "aac", "wma"];
let currentFileType = null;

function UploadFilePage() {
  const [data, setData] = useState([{}]);
  const [linkToResults, setLinkToResults] = useState(false);
  const navigate = useNavigate();
  const [acceptedTypes, setAcceptedTypes] = useState("");
  const [fileName, setFileName] = useState("");
  const [chosenButton, setChosenButton] = useState("video");
  const [fileUploaded, setFileUploaded] = useState(false);
  const [buttonPressed, setButtonPressed] = useState(false);
  const [showDetectButton, setShowDetectButton] = useState(false);

  const { username, setUsername } = useContext(AuthContext);




  const [dataURL, setDataURL] = useState(null);
  const [uploadedURL, setUploadedURL] = useState(null);

  console.log("***********************************");
  console.log("Accepted types: " + acceptedTypes);
  console.log("chosenButton: " + chosenButton);
  console.log("fileUploaded: " + fileUploaded);
  console.log("buttonPressed: " + buttonPressed);
  console.log("showDetectButton: " + showDetectButton);


  console.log("***********************************");







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
  const [detectionType, setDetectionType] = useState("");

  useEffect(() => {
    if (chosenButton)
      fileUploadedButtonClicked();
  }, [chosenButton]);

  const onDrop = useCallback(acceptedFiles => {
    acceptedFiles.forEach(file => {
      const reader = new FileReader();
      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');
      reader.onload = () => {
        const binaryStr = reader.result;
        setDataURL(binaryStr);
      };
      reader.readAsDataURL(file);
      handleFileChange({ target: { files: [file] } });
    });
  }, []);

  const {
    getRootProps,
    acceptedFiles,
    isDragActive,
    getInputProps,

  } = useDropzone({ onDrop });


  function handleFileChange(event) {
    console.log("File Name:" + event.target.files[0].name);
    const file = event.target.files[0];
    var filetype = file.name.split('.').pop();
    setFileName(file.name);

    currentFileType = filetype;

    let filename = file.name;
    if (filename.length > 40) {
      filename = filename.substring(0, 40) + "...";
    }
    console.log("Filetype uploaded: " + file.name.split('.').pop());

    if (ACCEPTED_VIDEO_TYPES.includes(currentFileType) || ACCEPTED_AUDIO_TYPES.includes(currentFileType)) {
      setSelectedFile(file);
      setShowCheckmark(true);
      setShowError(false);
      upload_p_ref.current.innerHTML = "Uploaded " + filename + " successfully!";
      upload_span_ref.current.innerHTML = "Click to change to another file.";
      // Update UI with selected file info
    } else {
      setSelectedFile(null);
      setShowCheckmark(false);
      setShowError(true);
      upload_p_ref.current.innerHTML = "File not supported!";
      upload_span_ref.current.innerHTML = "Please select a file of format: " + acceptedTypes;
    }
    setFileUploaded(true);
  };


  const handleSubmit = (event) => {

    if (!selectedFile) {
      setShowError(true);
      setUploadStatus('Please select a valid file');
      return;
    }


    const formData = new FormData();
    formData.append('uploaded_file', selectedFile);
    formData.append('detectionType', detectionType);



    const fetchResults = async () => {
      try {
        const response = await fetch('/Uploaded', {
          method: 'POST',
          body: formData, // Make sure formData is properly defined
        });
        const responseData = await response.json();
        setData(responseData.message);
        console.log(": " + detectionType);
        setLinkToResults(true);
        // Ensure we have all necessary data before navigating
        if (responseData && responseData[0] && responseData[1]) {
          navigate('/Results', {
            state: {
              videoURL: responseData[0],
              audioURL: responseData[1],
              fileType: currentFileType,
              detectionType: detectionType
            }
          });
        } else {
          console.error('Missing required data for navigation');
        }


      } catch (error) {
        //setData('Upload failed');
      }
    };
    fetchResults();

  };


  function buttonClicked(type) {
    setButtonPressed(true);
    switch (type) {
      case "videoAudio":
        videoAudioButtonRef.current.className = MainPage.ChoiceButtonActive;
        videoButtonRef.current.className = MainPage.ChoiceButton;
        audioButtonRef.current.className = MainPage.ChoiceButton;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #000000";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #ffffff";
        setDetectionType("va");
        break;
      case "video":
        videoAudioButtonRef.current.className = MainPage.ChoiceButton;
        videoButtonRef.current.className = MainPage.ChoiceButtonActive;
        audioButtonRef.current.className = MainPage.ChoiceButton;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #000000";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #ffffff";
        setDetectionType("v");
        break;
      case "audio":
        videoAudioButtonRef.current.className = MainPage.ChoiceButton;
        videoButtonRef.current.className = MainPage.ChoiceButton;
        audioButtonRef.current.className = MainPage.ChoiceButtonActive;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #000000";
        setDetectionType("a");
        break;
      default:
        console.log("Invalid button");
    }
    setChosenButton(type);
    fileUploadedButtonClicked();
  }


  function fileUploadedButtonClicked() {

    if (ACCEPTED_VIDEO_TYPES.includes(currentFileType)) {
      setShowCheckmark(true);
      setShowError(false);
      setShowDetectButton(true);
    } else if (ACCEPTED_AUDIO_TYPES.includes(currentFileType) && chosenButton === "audio") {
      setShowCheckmark(true);
      setShowError(false);
      setShowDetectButton(true);
    } else {
      setShowCheckmark(false);
      setShowError(true);
      setShowDetectButton(false);
    }
  }

  return (
    <div>
      <div className={PageDesign.mainDiv}>
        <h1 style={{ fontSize: "50px" }}>Upload a file</h1>
        <Link to="/profile"><button>Profile</button></Link>
        <Link to="/login"><button>login</button></Link>
        <Link to="/register"><button>register</button></Link>

        {/* {showCheckmark && <div>
          <ReactPlayer
            url={fileName}
            width="100%"
            height="300px"
            controls={true}
          />
          {console.log("File name: " + fileName)}
        </div>} */}

        <p>Upload a video or audio file for detection. Supported video formats: mp4, mvk, avi, mov. supported audio formats: wav, mp3. </p>



        {/* 
        <form onSubmit={handleSubmit} htmlFor="input-file" encType="multipart/form-data">
          <input type="file" name='uploaded_file' accept="mp4,mkv,avi,mov,wav,mp3" className={MainPage.inputFile} ref={inputFileRef} onChange={handleFileChange} />
          <button type="submit" className={MainPage.uploadButton}>Upload</button>
        </form>
        {uploadStatus && <p>{uploadStatus}</p>}
        {linkToResults && <Link to={`/Results?data=${data}`}>Go to results</Link>}
 */}




        <div className={MainPage.Dropzone}>
          <div className={MainPage.dropArea}  {...getRootProps()} onInput={handleFileChange} >
            <input {...getInputProps()} onChange={handleFileChange} ref={inputFileRef} />
            {isDragActive ? (
              <div className={MainPage.uploadImageDivDraggable} ref={imageDivRef}>
                <MdOutlineFileDownload className={MainPage.uploadImage} />

                <p>Drop the file here ...</p>

              </div>
            ) : (
              <div className={MainPage.uploadImageDiv} ref={imageDivRef}>
                {showCheckmark && <FaRegCheckCircle className={MainPage.uploadImage} id={MainPage.Checkmark} />}
                {showError && <VscError className={MainPage.uploadImage} id={MainPage.Error} />}
                {!showError && !showCheckmark && <FaCloudUploadAlt className={MainPage.uploadImage} />}
                <p ref={upload_p_ref}>Click or drop a file here.</p>
                <span ref={upload_span_ref}>Upload a video or audio file for detection.</span>

              </div>
            )}
          </div>
          {fileUploaded && <div className={MainPage.DetectionTypeChoiceDiv}>

            <div ref={videoAudioButtonRef} className={MainPage.ChoiceButton} onClick={(event) => { buttonClicked("videoAudio"); event.preventDefault(); }}>
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
            <div ref={videoButtonRef} className={MainPage.ChoiceButton} onClick={(event) => { buttonClicked("video"); event.preventDefault(); }}>
              <h2 style={{ display: "flex", justifyContent: "center", flexDirection: "column", marginRight: "20px" }}>Video</h2>

              <div ref={iconChoiceDivVideoRef} style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderLeft: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingLeft: "30px" }}>
                <GoVideo style={{ height: "40px", width: "40px" }} />

              </div>
            </div>
            <div ref={audioButtonRef} className={MainPage.ChoiceButton} onClick={(event) => { buttonClicked("audio"); event.preventDefault(); }}>
              <h2 style={{ display: "flex", justifyContent: "center", flexDirection: "column", marginRight: "20px" }}>Audio</h2>

              <div ref={iconChoiceDivAudioRef} style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px", borderLeft: "2px solid #ffffff", height: "100%", justifyContent: "center", paddingLeft: "30px" }}>
                <PiWaveformThin style={{ height: "40px", width: "40px" }} />
              </div>
            </div>

          </div>}
          {showCheckmark && buttonPressed && showDetectButton && <button onClick={handleSubmit} className={MainPage.uploadButton}>Detect</button>}
          {<button onClick={handleSubmit} className={MainPage.uploadButton}>Detect</button>}

        </div>
      </div >
    </div >
  );
}

export default UploadFilePage;