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


const ACCEPTED_VIDEO_TYPES = ["mp4", "mkv", "avi", "mov"];
const ACCEPTED_AUDIO_TYPES = ["wav", "mp3", "m4a", "flac", "ogg", "aac", "wma"];

function UploadFilePage() {
  const [data, setData] = useState([{}]);
  const [linkToResults, setLinkToResults] = useState(false);
  const [fileType, setFileType] = useState("videoAudio");
  const navigate = useNavigate();
  const [acceptedTypes, setAcceptedTypes] = useState("");


  const [dataURL, setDataURL] = useState(null);
  const [uploadedURL, setUploadedURL] = useState(null);




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
    const file = event.target.files[0];
    let filename = file.name;
    if (filename.length > 40) {
      filename = filename.substring(0, 40) + "...";
    }

    
    const ACCEPTED_FILE_TYPES = (fileType === "audio" ? ACCEPTED_AUDIO_TYPES : ACCEPTED_VIDEO_TYPES);

    console.log("Filetype uploaded: " + file.name.split('.').pop());
    console.log("Accepted file types: " + ACCEPTED_FILE_TYPES);
        
    if (file && ACCEPTED_FILE_TYPES.includes(file.name.split('.').pop())) {
      setSelectedFile(file);
      setShowCheckmark(true);
      setShowError(false);
      upload_p_ref.current.innerHTML = "Uploaded " + filename + " successfully!";
      upload_span_ref.current.innerHTML = "Click to change to another file.";
      // Update UI with selected file info
    } else {
      upload_p_ref.current.innerHTML = "File not supported!";
      upload_span_ref.current.innerHTML = "Please select a file of format: " + acceptedTypes;
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
        navigate('/Results', { state: { videoURL: responseData[0], audioURL: responseData[1] , fileType: fileType} });

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
        setFileType("videoAudio");
        setAcceptedTypes(ACCEPTED_VIDEO_TYPES.join(", "));
        break;
      case "video":
        videoAudioButtonRef.current.className = MainPage.ChoiceButton;
        videoButtonRef.current.className = MainPage.ChoiceButtonActive;
        audioButtonRef.current.className = MainPage.ChoiceButton;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #000000";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #ffffff";
        setFileType("video");
        setAcceptedTypes(ACCEPTED_VIDEO_TYPES.join(", "));
        break;
      case "audio":
        videoAudioButtonRef.current.className = MainPage.ChoiceButton;
        videoButtonRef.current.className = MainPage.ChoiceButton;
        audioButtonRef.current.className = MainPage.ChoiceButtonActive;
        iconChoiceDivVideoAudioRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivVideoRef.current.style.borderLeft = "2px solid #ffffff";
        iconChoiceDivAudioRef.current.style.borderLeft = "2px solid #000000";
        setFileType("audio");
        setAcceptedTypes(ACCEPTED_AUDIO_TYPES.join(", "));
        break;
      default:
        console.log("Invalid button");
    }
  }

  return (
    <div>
      <div className={PageDesign.mainDiv}>
        <h1 style={{ fontSize: "50px" }}>Upload a file</h1>
        <Link to="/profile"><button>Profile</button></Link>
        <Link to="/login"><button>login</button></Link>
        <Link to="/register"><button>register</button></Link>


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

        <label>Upload a file of type: {acceptedTypes}</label>


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
            <input type="file" name='uploaded_file' accept="mp4,mkv,avi,mov,wav,mp3,m4a,flac,ogg,aac,wma" className={MainPage.inputFile} ref={inputFileRef} onChange={handleFileChange} value=""/>
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
          {showCheckmark && <button onClick={handleSubmit} className={MainPage.uploadButton}>Detect</button>}
        </div>
      </div >
    </div >
  );
}

export default UploadFilePage;