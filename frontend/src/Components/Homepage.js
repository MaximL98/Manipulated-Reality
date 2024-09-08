import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import ExplenationPageStyle from '../Styles/ExplenationStyle.module.css';

function Homepage() {
  return (
    <div className={PageDesign.mainDiv}>
      <div className={ExplenationPageStyle.explenationDiv}>
        <h1>Welcome to Manipulated Reality!</h1>
        <div> <p>Some explanation here.</p></div>
      </div>
    </div>
  );
}

export default Homepage;