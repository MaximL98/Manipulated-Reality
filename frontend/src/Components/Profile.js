import React, { useState, useEffect } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';

function Profile() {
    const [data, setData] = useState({
        username: '',
        detectionData: [],
      });
    
      useEffect(() => {
        fetch('user_data.json')
          .then((response) => response.json())
          .then((jsonData) => {
            setData(jsonData);
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
      }, []);
    
    return (
        <>
            <div className={PageDesign.mainDiv}>
            <div>
                <h1>My Previous Tests</h1>
                <ul>
                    {data.detectionData.map((file, index) => (
                    <li key={index}>
                        <strong>Detection Type:</strong> {file.Detection_Type}<br />
                        <strong>Video Tested:</strong> {file.Video_Tested}<br />
                        <strong>Video Path:</strong> {file.Video_Path}<br />
                        <strong>Results:</strong> {file.Results}
                    </li>
                    ))}
                </ul>
                </div>
        </div>
        </>
    )
}

export default Profile;