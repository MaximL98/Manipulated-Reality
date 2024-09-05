import React, { useState, useEffect } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';

function Profile() {
  const [data, setData] = useState({
    username: 'c1',
    detectionData: [],
  });
  const [receivedData, setReceivedData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [updateResults, setUpdateResults] = useState(false);

  useEffect(() => {
    const form = new FormData();
    form.append('username', data.username);

    fetch('/user_data', { method: 'POST', body: form })
      .then((response) => response.json())
      .then(jsonData => {
        setReceivedData(jsonData.data);
        setIsLoading(false);
        setUpdateResults(true);
        console.log(jsonData);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });

    console.log(receivedData[0]);
  }, []);

  // useEffect(() => {
  //   fetch('/user_data', { method: 'POST', body: new FormData().append('username', data.username) })
  //   .then((response) => setReceivedData(response));
  // }, []);

  return (
    <>
      <div className={PageDesign.mainDiv}>
        <h1>My Previous  Tests</h1>

        <div className={PageDesign.ListLoadingDiv}>
            {isLoading ? (
              <p>Loading...</p>
            ) : (
              <>
                {updateResults && receivedData.map((file, index) => (
                  <div key={index} className={PageDesign.resultsListDiv}>
                    <li className={PageDesign.list}>
                      <strong className={PageDesign.listItem}>Detection Type:</strong> {file.Detection_Type}
                      <strong className={PageDesign.listItem}>Video Tested:</strong> {file.Video_Tested}
                      <strong className={PageDesign.listItem}>Video Path:</strong> {file.Video_Path}
                      <strong className={PageDesign.listItem}>Results:</strong> {file.Results}
                    </li>
                  </div>

                ))}
              </>
            )}

        </div>
      </div>
    </>
  )
}

export default Profile;