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
  const [filesTested, setFilesTested] = useState([]);





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
      setFilesTested(receivedData.Video_Tested.split(','));

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

  }, [receivedData])



  // useEffect(() => {
  //   fetch('/user_data', { method: 'POST', body: new FormData().append('username', data.username) })
  //   .then((response) => setReceivedData(response));
  // }, []);

  return (
    <>
      <div className={PageDesign.mainDiv}>
        <h1>{username}'s profile</h1>
        <div className={PageDesign.ListLoadingDiv}>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <>
              <div>
                <h2 style={{ left: "13%" }}>Previous prediction processes:</h2>
                <div className={PageDesign.listDivWrapper}>
                  {updateResults && filesTested.map((file, index) => (
                    <div>
                      {detectionType[index] && <div className={PageDesign.listDiv}>
                        <div key={index} className={PageDesign.resultsListDiv}>
                          <li className={PageDesign.list}>
                            <strong className={PageDesign.listItem}>File name: {filesTested[index]}</strong>
                            <strong className={PageDesign.listItem}>Detection Type: {detectionType[index]}</strong>
                            <strong className={PageDesign.listItem}>Real probability: {parseFloat(results[index] * 100).toFixed(2)}%</strong>
                          </li>
                        </div>
                      </div>}
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