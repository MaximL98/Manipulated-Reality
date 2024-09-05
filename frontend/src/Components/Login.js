import React from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import Navbar from './Navbar';

function Login() {
    return (
        <>
            <div className={PageDesign.mainDiv}>
      <div>
        <h1>Login</h1>
        <form method="POST" action="/loginUser">
          <label htmlFor="username">Username:</label>
          <input type="text" name="username" required />

          <label htmlFor="password">Password:</label>

          <input type="password" name="password" required />

          <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register here</a></p>
      </div>
            </div>
        </>
    )
}

export default Login;