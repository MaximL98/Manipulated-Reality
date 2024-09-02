import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';

function About() {
    return (
        <>
            <div className={PageDesign.mainDiv}>
                <h1>About Page</h1>
                <p>Here is an explenation</p>
            </div>
        </>
    )
}

export default About;