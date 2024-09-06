import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';
import RegisterBlock from './RegisterBlock.js';

function Register() {
    return (
        <>
        <RegisterBlock/>
            <div className={PageDesign.mainDiv}>
            <div>
        <h1>Register</h1>
        <form method="POST" action="/register">
          <label htmlFor="username">Username:</label>
          <input type="text" name="username" required />

          <label htmlFor="password">Password:</label>
          <input type="password" name="password" required />

          <label htmlFor="email">Email:</label>
          <input type="email" name="email" required />


          <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="/login">Login here</a></p>
      </div>
        </div>
        </>
    )
}

export default Register;