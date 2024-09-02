import React, { useEffect, useReducer, useState} from "react";
import { useLocation } from "react-router-dom";
import formData from './UploadFilePage.js';
import Navbar from './Navbar.js';
import PageDesign from '../Styles/PageDesign.module.css';
import CircleLoader from './LoadingComponents/CircleLoader.js'
import { Link } from 'react-router-dom';


function Results() {
    const [data, setData] = useState([{}]);
    const [isLoading, setIsLoading] = useState(true);
    const { formData } = useLocation().state;
    let i = 0;

    useEffect(() => {

        // let intervalId;
        // const fetchResults = async () => {
        //     setIsLoading(true);
        //     try {
        //         const response = await fetch('/Results', {
        //             method: 'POST',
        //             body: formData // Make sure formData is properly defined
        //         });
        //         const responseData = await response.json();
        //         setData(responseData.message);
        //         setIsLoading(false);
        //     } catch (error) {
        //         console.error('Error:', error);
        //         setData('Upload failed');
        //         setIsLoading(false);
        //     }
        // };
        // if (data.message !== 'Succssfuly uploaded dadada') {
        //     intervalId = setInterval(fetchResults, 5000);
        // }
        // return () => {
        //     clearInterval(intervalId);
        //   };
        

    // fetch('/Results', {
    //   method: 'POST',
    //   body: formData,
    // })
    //   .then(response => response.json())
    //   .then(data => {
    //     setUploadStatus(data.message);
    //     console.log(data);
    //   })
    //   .catch(error => {
    //     console.error('Error:', error);
    //     setUploadStatus('Upload failed');
    //   });
    }, []);



    return (
        <>
            {/* <Navbar /> */}
            <div className={PageDesign.mainDiv}>
                {!isLoading ? (
                    <CircleLoader />
                ) : (
                    <div>
                        {data === null ? (
                            <p>No data received</p>
                        ) : (
                            <p>{formData}</p>
                        )}
                        <h1>Results for {/*data.name*/}</h1>
                        <h2>Video certainty: {/*data.video*/}% fake</h2>
                        <h2>Audio certainty: {/*data.audio*/}% fake</h2>
                        <h2>Total certainty: {/*data.image*/}% fake</h2>

                        <p>The results are saved in <Link to="/profile">My profile</Link> and could be viewed later.</p>

                        <Link to="/"><button>Upload another file</button></Link>
                        <div>                        <button>Expand information</button>
                        </div>
                    </div>
                    
                )}
            </div>
        </>
    );
}

export default Results;