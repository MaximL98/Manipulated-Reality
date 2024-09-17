import React from "react";
import PageDesign from "../Styles/PageDesign.module.css";
import ExplenationPageStyle from "../Styles/ExplenationStyle.module.css";
import { Link } from "react-router-dom";

function About() {
  return (
    <>
      <div className={PageDesign.mainDiv}>
        <div className={ExplenationPageStyle.explenationDiv}>
          <h2>How to use our site</h2>
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
          <img src="ResultsPage.png" alt="Results Page" className={ExplenationPageStyle.image} style={{ maxWidth: "550px" }} />
          <p><br></br><br></br>Navigate to <Link to="/profile">your profile</Link> by clicking on the icon in the top right corner.</p>
          <img src="MyProfile.png" alt="Profile Page" className={ExplenationPageStyle.image} style={{ maxWidth: "350px" }} />
          <br></br>
          <br></br>
          <br></br>
          <h3>We put a lot of hard work into this project. We certainly hope you will like it!</h3>
          <p>Developed by: <Link to="https://github.com/MaximL98">Maxim Lebedinsky</Link>, <Link to="https://github.com/DimaKyn">Dima Kislitsyn</Link>.</p>

        </div>
        <div className={ExplenationPageStyle.explenationDiv}>
          <h1>Development process</h1>
          <p>
            This development and research project aims to contribute to the
            ongoing efforts to combat the generation of deepfakes.
          </p>
          <p>
            We present a novel framework for the detection of deepfake media that involves
            two distinct models: A hybrid deep learning architecture utilizing
            the Keras framework for the classification of deepfake content.
          </p>
          <p>
            The framework incorporates a pre-trained InceptionV3 model for video
            feature extraction, followed by a Long Short-Term Memory (LSTM)
            network to capture temporal dependencies. Additionally, by utilizing
            the frameworks SoundFile and Librosa, which are used for processing
            audio, we feed the processed audio into a sequential CNN model for
            identifying fake speech.
          </p>
          <p>
            By combining these models through
            statistical analysis, we can effectively detect deepfakes that
            incorporate both visual and auditory manipulations. We can also
            consider cases involving solely video or audio sources. Our
            experimental results demonstrate an accuracy of approximately 83%
            for detection of video-based deepfakes and 92% of audio-based
            deepfakes.
          </p>
          <p>
            To ensure widespread accessibility, we have developed a
            user-friendly web application that allows users to upload suspected
            deepfake content and receive a probability score indicating its
            authenticity. To further enhance the model's performance, a
            comprehensive hyperparameter optimization study is recommended
            exploring various combinations of parameters such as loss function,
            number of epochs, learning rate etc.
          </p>
          <p>
            Additionally, augmenting the
            training dataset with a diverse range of video and audio content
            could be beneficial.
          </p>
          <h2>Development Pipeline</h2>
          <img src="project_pipeline.png" alt="Project Pipeline Image" className={ExplenationPageStyle.image} />

          <h2>Video Model</h2>
          <p>
            The development used a dataset (Celeb-DF-V2) of authentic and deepfake videos to
            train a deepfake detection model. The videos were preprocessed to
            extract facial regions and standardize frame rates. A fine-tuned
            Inception V3 model extracted features from the video frames, which
            were then used to train an LSTM model for deepfake detection.
          </p>
          <h2>Audio Model</h2>
          <p>
            The model was trained on three datasets totaling over 50 hours of
            audio to maximize its familiarity with various speeches. Each audio
            sample was preprocessed by extracting 100 MFCC coefficients and
            calculating delta and delta^2 features, resulting in a vector of
            13200 values. These vectors were stored in Numpy files for training
            the audio detection model.
          </p>
          <h2>Used Technologies</h2>
          <div className={ExplenationPageStyle.gridLayout}>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="Google_Colaboratory_Logo.png" alt="Google Colaboratory Logo" className={ExplenationPageStyle.imageLogo} style={{ width: "100%" }} />
            </div>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="Keras_Logo.png" alt="Keras Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />

            </div>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="react_Logo.png" alt="React Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />

            </div>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="flask_logo.png" alt="Flask Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />

            </div>
          </div>
          <div className={ExplenationPageStyle.gridLayout}>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="tensofrlow_logo.png" alt="Tensorflow Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />

            </div>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="Python_logo.png" alt="Python Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />

            </div>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="sqlite_logo.png" alt="SQLite Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />

            </div>
            <div className={ExplenationPageStyle.logoDiv}>
              <img src="Node.js_logo.png" alt="Node.js Logo" className={ExplenationPageStyle.imageLogo} style={{ height: "auto", width: "100%" }} />
            </div>


          </div>

        </div>
      </div>
    </>
  );
}

export default About;
