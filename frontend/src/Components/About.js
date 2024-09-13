import React from "react";
import PageDesign from "../Styles/PageDesign.module.css";
import ExplenationPageStyle from "../Styles/ExplenationStyle.module.css";

function About() {
  return (
    <>
      <div className={PageDesign.mainDiv}>
        <div className={ExplenationPageStyle.explenationDiv}>
          <h1>About Page</h1>
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
          <p>Put logos of things we used for this project</p>
        </div>
      </div>
    </>
  );
}

export default About;
