import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';

function About() {
    return (
        <>
            <div className={PageDesign.mainDiv}>
                <h1>About Page</h1>
                <p>This research presents a novel framework for the detection of deepfake media,
                   a growing concern due to its potential for misinformation and harmful content. 
                   Our approach involves two distinct models: a computer vision-based model for 
                   detecting deepfake videos and an audio processing model utilizing MFCC feature extraction for identifying fake speech.
                   By combining these models through statistical analysis, 
                   we can effectively detect deepfakes that incorporate both visual and auditory manipulations
                   while also considering cases involving solely video or audio formats.
                   To ensure widespread accessibility,
                   we have developed a user-friendly web application that allows users to upload suspected deepfake content
                  and receive a probability score indicating its authenticity.
                 This framework aims to contribute to the ongoing efforts to combat the generation of deepfakes and empower individuals and developers to enhance detection capabilities and protect against their harmful consequences.
</p>
            </div>
        </>
    )
}

export default About;