import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import ExplenationPageStyle from '../Styles/ExplenationStyle.module.css';
import { Link } from 'react-router-dom';
import { AuthContext } from './AuthProvider';

function Homepage() {
  const { username } = React.useContext(AuthContext);
  return (
    <div className={PageDesign.mainDiv}>
      <div className={ExplenationPageStyle.explenationDiv}>
        <h1>Welcome to Manipulated Reality!</h1>
        <div> {username ? (
          <div>
            <p style={{ textAlign: "center" }}>Welcome back, {username}!</p>
          </div>
        ) : (
          <div>
            <p style={{ textAlign: "center" }}>Not logged in</p>
            <p style={{ textAlign: "center" }}><Link to="/Login">Login</Link> or <Link to="/Register">register</Link> to start detecting deepfake video and audio!</p>
          </div>)}
        </div>
      </div>
      <div className={ExplenationPageStyle.explenationDiv}>
        <h2>Our purpose</h2>
        <p>
          Manipulated Reality is a web application that allows users to upload suspected deepfake content and receive a probability score indicating its authenticity.
          <br></br>
          Our model is trained to detect deepfake content in both video and audio files.
        </p>
        <h3>How to use</h3>
        <p>
          Once you log in or create a new account, navigate to the upload page which is located in the navigation bar menu, on the top left corner.
        </p>
        <img src="HamburgerMenu.png" alt="Hamburger Menu" className={ExplenationPageStyle.image} style={{ maxWidth: "150px" }} />
        <p>
          From there, you can navigate to the file upload page. There, you will be albe to upload your video or audio file and select the type of detection you would like to perform (video & audio, video only, audio only).
        </p>
        <img src="NavbarUploadButton.png" alt="Upload Page" className={ExplenationPageStyle.image} style={{ maxWidth: "350px" }} />

        <img src="FileUploaded.png" alt="Results Page" className={ExplenationPageStyle.image} style={{ maxWidth: "1050px" }} />
        <p>
          Once you have uploaded your file, you will be redirected to the results page where you can see the probability score of your file.
          Remember that the results are saved in your profile page, so you can always come back and check them later.
        </p>
        <img src="ResultsPage.png" alt="Results Page" className={ExplenationPageStyle.image} style={{ maxWidth: "1050px" }} />
        <p><br></br><br></br>Navigate to <Link to="/profile">your profile</Link> by clicking on the icon in the top right corner.</p>
        <img src="MyProfile.png" alt="Profile Page" className={ExplenationPageStyle.image} style={{ maxWidth: "350px" }} />
        <br></br>
        <br></br>
        <br></br>
        <h3>We put a lot of hard work into this project. We certainly hope you will like it!</h3>
        <p>Developed by: <Link to="https://github.com/MaximL98">Maxim Lebedinsky</Link>, <Link to="https://github.com/DimaKyn">Dima Kislitsyn</Link>.</p>

      </div>

    </div>
  );
}

export default Homepage;