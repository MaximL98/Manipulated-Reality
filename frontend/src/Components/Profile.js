import React, { useState, useEffect } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import { AuthContext } from './AuthProvider';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

function Profile() {
  const { username, setUsername } = useContext(AuthContext);
  const navigate = useNavigate();

  const [receivedData, setReceivedData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [updateResults, setUpdateResults] = useState(false);

  const [detectionType, setDetectionType] = useState([]);
  const [results, setResults] = useState([]);
  const [videoPath, setVideoPath] = useState([]);
  const [videosTested, setVideosTested] = useState([]);


  useEffect(() => {
    if (username === '') {
      navigate('/Login');
    }
    const form = new FormData();
    form.append('username', username);
    console.log(username);

    fetch('/user_data', { method: 'POST', body: form })
      .then((response) => response.json())
      .then(jsonData => {
        setReceivedData(jsonData.data[0]);
        setIsLoading(false);
        setUpdateResults(true);
        console.log(jsonData.data[0]);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });

  }, []);

  useEffect(() => {
    console.log(typeof (receivedData.Detection_Type));
    if (receivedData.Detection_Type) {
      console.log(typeof (receivedData.Detection_Type));

      setResults(receivedData.Results.split(','));
      setVideoPath(receivedData.Video_Path.split(','));
      setVideosTested(receivedData.Video_Tested.split(','));

      let detectionTypeList = receivedData.Detection_Type.split(',');

      for (let i = 0; i < detectionTypeList.length; i++) {
        switch (detectionTypeList[i]) {
          case 'va':
            detectionTypeList[i] = 'Video & Audio Detection';
            break;
          case 'v':
            detectionTypeList[i] = 'Video Detection';
            break;
          case 'a':
            detectionTypeList[i] = 'Audio Detection';
            break;
          default:
            detectionTypeList[i] = 'Error';
            break
        }
      }
      setDetectionType(receivedData.Detection_Type.split(','));
    }
    // console.log("ref " + receivedData.Results.split(','));
    // for (let i = 0; i < receivedData.Detection_Type.split(',').length; i++) {
    // console.log(detectionType.push(receivedData.Detection_Type.split(',')[1]));
    // console.log(results.push(receivedData.Results.split(',')[1]));
    // console.log(videoPath.push(receivedData.Video_Path.split(',')[1]));
    // console.log(videosTested.push(receivedData.Video_Tested.split(',')[1]));
    // }
  }, [receivedData])



  // useEffect(() => {
  //   fetch('/user_data', { method: 'POST', body: new FormData().append('username', data.username) })
  //   .then((response) => setReceivedData(response));
  // }, []);

  return (
    <>
      <div className={PageDesign.mainDiv}>
        <h1>Hi {username}, this is your profile.</h1>


        <div className={PageDesign.ListLoadingDiv}>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <>
              <div>
                <h2 style={{ left: "13%" }}>This table lists your previous detection processes.</h2>
                <div style={{}}>
                  {updateResults && videosTested.map((file, index) => (
                    <div key={index} className={PageDesign.resultsListDiv}>
                      <li className={PageDesign.list}>
                        <strong className={PageDesign.listItem}>Detection Type:</strong> {detectionType[index]}
                        <strong className={PageDesign.listItem}>Video Tested:</strong> {videosTested[index]}
                        <strong className={PageDesign.listItem}>Video Path:</strong> {videoPath[index]}
                        <strong className={PageDesign.listItem}>Results:</strong> {results[index]}
                      </li>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

        </div>
      </div>
    </>
  )
}

export default Profile;