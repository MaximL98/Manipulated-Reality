import React, { useState, useEffect } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';
import { AuthContext } from './AuthProvider';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

function Profile() {
  const { username, setUsername } = useContext(AuthContext);
  const navigate = useNavigate();

  const [receivedData, setReceivedData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [updateResults, setUpdateResults] = useState(false);

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
        <h1>Hi {username}, this is your profile.</h1>


        <div className={PageDesign.ListLoadingDiv}>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <>
              <div>
                <h2 style={{ left: "13%" }}>This table lists your previous detection processes.</h2>
                <div style={{ }}>
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