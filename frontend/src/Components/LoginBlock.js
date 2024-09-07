import Style from '../Styles/LoginBlock.module.css';
import { FaUserAlt, FaKey } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import React, { useState, useEffect, useRef } from 'react';
import { BiLoader } from 'react-icons/bi';

import { AuthContext } from './AuthProvider';
import { useContext } from 'react'; 

// Removed unused sleep function

function LoginBlock() {
  const { setUsername, setToken, username , token} = useContext(AuthContext);



  const [usernameClient, setUsernameClient] = useState('');
  const [password, setPassword] = useState('');
  const loginButtonRef = useRef(null);
  const incorrectCredentialsLabelRef = useRef(null);
  const [loginText, setLoginText] = useState('Login');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const loadingIconRef = useRef(null);
  const navigate = useNavigate();

  

  function handleKeyPress(e) {
    if (e.key === 'Enter') {
      handleLogin();
    }
  }

  async function handleLogin() {
    const form = new FormData();
    form.append('username', usernameClient);
    form.append('password', password);

    await fetch('/loginUser', {
      method: 'POST',
      body: form
    })
      .then((response) => response.json())
      .then(jsonData => {
        if (jsonData === "USER FOUND") {
          setUsername(usernameClient);

          console.log("JSON response: " + jsonData)
          console.log("username: ", username)
          setIsLoggedIn(jsonData.isLoggedIn);
          setToken(jsonData.token);
          navigate('/profile');
        }
        else {

        }
        console.log(jsonData);
      }).catch((error) => {
        console.error('Error logging in:', error);
      });

    if (usernameClient === '' || password === '') {
      return;
    }
    setLoginText('Logging in');
    loginButtonRef.current.disabled = true;
    loadingIconRef.current.className = Style.loginButtonIconLoading;
    // Removed sleep function call
    setLoginText('Login');
    loginButtonRef.current.disabled = false;
    loadingIconRef.current.className = Style.loginButtonIconIdle;
    incorrectCredentialsLabelRef.current.style.display = 'block';
  }

  useEffect(() => {
    if (username !== '') {
        navigate('/profile');
    }
}, [username]);

  return (
    <>
      <div className={Style.loginBlock}>
        <label className={Style.loginLabel}>LOGIN</label>
        <div className={Style.usernameBlock}>
          <FaUserAlt className={Style.userIcon} />
          <input
            required
            pattern=".*\S.*"
            type="text"
            className={Style.usernameInput}
            value={usernameClient}
            onChange={(e) => setUsernameClient(e.target.value)}
            onKeyDown={handleKeyPress}
          />
          <label className={Style.usernameLabel}>Username/Email</label>
        </div>
        <div className={Style.passwordBlock}>
          <FaKey className={Style.passwordIcon} />
          <input
            required
            pattern=".*\S.*"
            type="password"
            className={Style.passwordInput}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKeyPress}
          />
          <label className={Style.passwordLabel}>Password</label>
        </div>
        <div className={Style.buttonDiv}>
          <button
            ref={loginButtonRef}
            className={Style.loginButton}
            onClick={handleLogin}
          >
            <div ref={loadingIconRef} className={Style.loginButtonIconIdle}>
              <BiLoader />
            </div>
            {loginText}
          </button>
          <label ref={incorrectCredentialsLabelRef} className={Style.incorrectCredentialsLabel}>
            Incorrect Username or Password
          </label>
          <label style={{ fontSize: '20px', color: "rgba(80, 80, 250, 1)" }}>
            New to Manipulated Reality?
          </label>
          <Link to="/Register" className={Style.registerButton}>
            Register now
          </Link>
        </div>
      </div>
    </>
  );
}

export default LoginBlock; // Corrected export statement
