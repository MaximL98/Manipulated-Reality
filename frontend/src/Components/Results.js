import React, { useEffect, useReducer, useState } from "react";
import formData from './UploadFilePage.js';
import PageDesign from '../Styles/PageDesign.module.css';
import CircleLoader from './LoadingComponents/CircleLoader.js'
import { Link } from 'react-router-dom';
import { useParams } from 'react-router-dom';

import { useLocation } from "react-router-dom";




function Results() {
    const [isLoading, setIsLoading] = useState(true);
    const [results, setResults] = useState([]);
    const [displayData, setDisplayData] = useState(false);
    const location = useLocation();

    console.log(location);
    const audioURL = location.state.audioURL;
    const videoURL = location.state.videoURL;


    const form = new FormData();
    form.append('audioURL', audioURL);
    form.append('videoURL', videoURL);

    useEffect((event) => {
        fetch('/Results', {
            method: 'POST',
            body: form
        })
            .then(response => response.json())
            .then(data => {
                setResults(data);
                setIsLoading(false);
                setDisplayData(true);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, [location]);

    return (
        <>            
            <div className={PageDesign.mainDiv}>
                {isLoading ? (
                    <CircleLoader />
                ) : (
                    <div>
                        <h1>Results for {/*data.name*/}</h1>
                        <h2>Video certainty: {displayData && results[0]}% real</h2>
                        <h2>Audio certainty: {displayData && results[1]}% real</h2>

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