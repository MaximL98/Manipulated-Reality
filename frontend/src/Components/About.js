import React from "react";
import PageDesign from "../Styles/PageDesign.module.css";
import Navbar from "./Navbar";
import ExplenationPageStyle from "../Styles/ExplenationStyle.module.css";

function About() {
  return (
    <>
      <div className={PageDesign.mainDiv}>
        <div className={ExplenationPageStyle.explenationDiv}>
          <h1>About Page</h1>
          <p>
            This development and research project aims to contribute to the
            ongoing efforts to combat the generation of deepfakes. We present a
            novel framework for the detection of deepfake media that involves
            two distinct models: A hybrid deep learning architecture utilizing
            the Keras framework for the classification of deepfake content. The
            framework incorporates a pre-trained InceptionV3 model for video
            feature extraction, followed by a Long Short-Term Memory (LSTM)
            network to capture temporal dependencies. Additionally, by utilizing
            the frameworks SoundFile and Librosa, which are used for processing
            audio, we feed the processed audio into a sequential CNN model for
            identifying fake speech. By combining these models through
            statistical analysis, we can effectively detect deepfakes that
            incorporate both visual and auditory manipulations. We can also
            consider cases involving solely video or audio sources. Our
            experimental results demonstrate an accuracy of approximately 83%
            for detection of video-based deepfakes and 92% of audio-based
            deepfakes. To ensure widespread accessibility, we have developed a
            user-friendly web application that allows users to upload suspected
            deepfake content and receive a probability score indicating its
            authenticity. To further enhance the model's performance, a
            comprehensive hyperparameter optimization study is recommended
            exploring various combinations of parameters such as loss function,
            number of epochs, learning rate etc. Additionally, augmenting the
            training dataset with a diverse range of video and audio content
            could be beneficial.
          </p>
          <h2>Development Pipeline</h2>
          <img src="project_pipeline.png" alt="Project Pipeline Image"/>
        </div>
      </div>
    </>
  );
}

export default About;
