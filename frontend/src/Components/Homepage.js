import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';

function Homepage() {
  return (
    <div className={PageDesign.mainDiv}>
      <h1>Welcome to Manipulated Reality!</h1>
      <div> <p>Some explanation here.</p></div>
    </div>
  );
}

export default Homepage;