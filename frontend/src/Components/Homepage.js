import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import ExplenationPageStyle from '../Styles/ExplenationStyle.module.css';
import { Link } from 'react-router-dom';
import { AuthContext } from './AuthProvider';
import MainPage from '../Styles/MainPage.module.css';

function Homepage() {
  const { username } = React.useContext(AuthContext);
  return (
    <div className={PageDesign.mainDiv}>
      <div className={ExplenationPageStyle.explenationDiv}>
        <h1>Welcome to Manipulated Reality!</h1>
        <div> {username ? (
          <div>
            <h3 style={{ textAlign: "center" }}>Welcome back, {username}!</h3>
            <Link to="/UploadFilePage" style={{marginTop: "0px", marginRight: "10px"}}><button className={MainPage.uploadButton}>Upload a deepfake</button></Link>
            <Link to="/About" style={{marginTop: "0px", marginRight: "10px"}}><button className={MainPage.uploadButton}>More info</button></Link>
            <Link to="/Profile" style={{marginTop: "0px", marginRight: "10px"}}><button className={MainPage.uploadButton}>My profile</button></Link>


            </div>
        ) : (
          <div>
            <h3 style={{ textAlign: "center" }}>Not logged in</h3>
            <p style={{ textAlign: "center" }}><Link to="/Login">Login</Link> or <Link to="/Register">register</Link> to start detecting deepfake video and audio!</p>
          </div>)}
        </div>
      </div>
      <div className={ExplenationPageStyle.explenationDiv}>
        <h2>Deepfake detection made simple</h2>
        <p>
          Manipulated Reality allows users to upload suspected deepfake content and receive a probability score indicating its authenticity.
          <br></br>
        </p>
        <img src="Deepfake.png" alt="Deepfake" className={ExplenationPageStyle.image} style={{ maxWidth: "600px" }} />

      </div>
      

    </div>
  );
}

export default Homepage;