import React, { useEffect } from 'react';
import PageDesign from '../Styles/PageDesign.module.css';
import { useContext } from 'react';
import { AuthContext } from './AuthProvider.js';
import { Link } from 'react-router-dom';
import LoginDesign from '../Styles/LoginDesign.module.css';
import LoginBlock from './LoginBlock.js';

function Login() {
  const { username, setUsername, token, setToken } = useContext(AuthContext);

  useEffect(() => {
    console.log(username);
  }, [username]);

  return (
    <>
    
      <div className={PageDesign.mainDiv}>
        <div className={LoginDesign.mainDiv}>
        <LoginBlock/>

          {/* <div className={LoginDesign.middleBox}>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
              <label htmlFor="username">Username:</label>
              <input type="text" name="username" required />

              <label htmlFor="password">Password:</label>

              <input type="password" name="password" required />

              <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="/register">Register here</a></p>
            <Link to="/profile">Profile</Link>
          </div> */}
        </div>
      </div>
    </>
  )
}

export default Login;