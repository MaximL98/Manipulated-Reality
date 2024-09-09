import React, { useEffect, useReducer, useState } from "react";
import formData from './UploadFilePage.js';
import PageDesign from '../Styles/PageDesign.module.css';
import CircleLoader from './LoadingComponents/CircleLoader.js'
import { Link } from 'react-router-dom';
import { useParams } from 'react-router-dom';

import { useLocation } from "react-router-dom";
import { AuthContext } from "./AuthProvider.js";
import { useContext } from "react";
import ReactPlayer from 'react-player';



function Results() {
    const [isLoading, setIsLoading] = useState(true);
    const [results, setResults] = useState([]);
    const [displayData, setDisplayData] = useState(true);
    const [videoFile, setVideoFile] = useState();
    const [videoResult, setVideoResult] = useState();
    const [audioResult, setAudioResult] = useState();

    const { username } = useContext(AuthContext);

    const location = useLocation();

    const audioURL = location.state.audioURL;
    const videoURL = location.state.videoURL;
    const detectionType = location.state.detectionType;
    const fileURL = location.state.fileURL;

    const [textDisplay, setTextDisplay] = useState("");


    const sentences = [
        "The model is analyzing the file.",
        "The model is analyzing the file..",
        "The model is analyzing the file...",
        "This may take a while.",
        "This may take a while..",
        "This may take a while...",
        "Larger videos may take longer to analyze.",
        "Larger videos may take longer to analyze..",
        "Larger videos may take longer to analyze...",
        "Sit back and relax while the model does its job.",
        "Sit back and relax while the model does its job..",
        "Sit back and relax while the model does its job...",
        "Grab some cookies and coffee while you wait.",
        "Grab some cookies and coffee while you wait..",
        "Grab some cookies and coffee while you wait...",

    ];

    let currentIndex = 0;

    useEffect(() => {
        const interval = setInterval(() => {
            setTextDisplay(sentences[currentIndex]);
            currentIndex = (currentIndex + 1) % sentences.length;
        }, 1000);

        return () => {
            clearInterval(interval);
        };
    }, []);



    let resultTypeString = "Results for ";
    switch (detectionType) {
        case "va":
            resultTypeString += "video and audio detection:";
            break;
        case "v":
            resultTypeString += "video detection:";
            break;
        case "a":
            resultTypeString += "audio detection:";
            break;
        default:
            break;

    }

    const form = new FormData();
    form.append('audioURL', audioURL);
    form.append('videoURL', videoURL);
    form.append('detectionType', detectionType);
    form.append('username', username);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const response = await fetch('/Results', { method: 'POST', body: form });
                const data = await response.json();
                switch (detectionType) {
                    case "va":
                        setVideoResult((parseFloat(data[0]) * 100).toFixed(2));
                        setAudioResult((parseFloat(data[1]) * 100).toFixed(2));
                        break;
                    case 'v':
                        setVideoResult((parseFloat(data[0]) * 100).toFixed(2));
                        break;
                    case 'a':
                        setAudioResult((parseFloat(data[0]) * 100).toFixed(2));
                        break;
                    default:
                        break;
                }
                setResults(data);
                setIsLoading(false);
                setDisplayData(true);
            } catch (error) {
                console.error('Error:', error);
            }
        }
        fetchResults();
    }, [location]);

    // useEffect((event) => {
    //     fetch('/Results', {
    //         method: 'POST',
    //         body: form
    //     })
    //         .then(response => { response.json() })
    //         .then(data => {
    //             console.log(data);
    //             switch (detectionType) {
    //                 case "va":
    //                     setVideoResult(results[0]);
    //                     setAudioResult(results[1]);
    //                     break;
    //                 case 'v':
    //                     setVideoResult(results);
    //                     break;
    //                 case 'a':
    //                     setAudioResult(results);
    //                     break;
    //                 default:
    //                     break;
    //             }
    //             setResults(data);
    //             setIsLoading(false);
    //             setDisplayData(true);
    //         })
    //         .catch((error) => {
    //             console.error('Error:', error);
    //         });
    // }, [location]);



    return (
        <>
            <div className={PageDesign.mainDiv}>
                <div className={PageDesign.ReactPlayer}>
                    {fileURL && (
                        <ReactPlayer url={fileURL} width="270px" height="480px" controls={true} style={{padding: "10px", borderRadius: "5px"}}/>
                    )}
                </div>
                {isLoading ? (<>
                    <CircleLoader />
                    <div style={{display: "flex", justifyContent: "center", justifyContent: "center", textAlign: "center"}}>
                        <h2>{textDisplay}</h2>

                    </div>
                </>
                ) : (
                    <div>
                        <h1>{resultTypeString}</h1>
                        {videoResult && <h2>Video certainty: {videoResult}% real</h2>}
                        {audioResult && <h2>Audio certainty: {audioResult}% real</h2>}

                        <p>The results are saved in <Link to="/profile">My profile</Link> and could be viewed later.</p>

                        <Link to="/"><button>Upload another file</button></Link>
                        <div>                        <button>Expand information</button>

                            <div>
                                {/* Display your data */}
                            </div>
                        </div>
                    </div>

                )}
            </div>
        </>
    );
}

export default Results;