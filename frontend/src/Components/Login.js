import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';

function About() {
    return (
        <>
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
      </div>
      <div>
        <h1>Login</h1>
        <form method="POST" action="/loginUser">
          <label htmlFor="username">Username:</label>
          <input type="text" name="username" required />

          <label htmlFor="password">Password:</label>

          <input type="password" name="password" required />

          <button type="submit">Login</button>
        </form>
      </div>
            </div>
        </>
    )
}

export default About;