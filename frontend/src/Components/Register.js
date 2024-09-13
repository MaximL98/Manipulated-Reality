import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar.js';
import RegisterBlock from './RegisterBlock.js';
import LoginDesign from '../Styles/LoginDesign.module.css';


function Register() {
  return (
    <>
      <div className={PageDesign.mainDiv}>
        <div className={LoginDesign.mainDiv}>
          <RegisterBlock />
        </div>
      </div>
    </>
  )
}

export default Register;