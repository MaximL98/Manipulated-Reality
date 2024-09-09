import Style from '../Styles/LoginBlock.module.css';
import { FaUserAlt, FaKey } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import React, { useState, useEffect, useRef } from 'react';
import { BiLoader } from 'react-icons/bi';
import { AuthContext } from './AuthProvider';
import { useContext } from 'react';


function LoginBlock() {
  const { setUsername, setToken, username, token } = useContext(AuthContext);

  const [usernameClient, setUsernameClient] = useState('');
  const [password, setPassword] = useState('');
  const loginButtonRef = useRef(null);
  const incorrectCredentialsLabelRef = useRef(null);
  const [loginText, setLoginText] = useState('Login');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const loadingIconRef = useRef(null);
  const navigate = useNavigate();


  function changeLoginAnimation(status) {
    switch (status) {
      case 'login':
        loadingIconRef.current.className = Style.loginButtonIconIdle;
        loginButtonRef.current.disabled = true;
        loginButtonRef.current.className = Style.loginButton;
        loginButtonRef.current.style.borderColor = 'green';
        loginButtonRef.current.style.color = 'rgb(144, 238, 144)';
        incorrectCredentialsLabelRef.current.disabled = true;
        setLoginText('Success!');
        break;
      case 'failed':
        loginButtonRef.current.className = Style.loginButton;
        loginButtonRef.current.disabled = false;
        loadingIconRef.current.className = Style.loginButtonIconIdle;
        incorrectCredentialsLabelRef.current.disabled = false;
        incorrectCredentialsLabelRef.current.className = Style.incorrectCredentialsLabelShow;
        setLoginText('Login');
        break;
      default:
        loginButtonRef.current.disabled = false;
        loadingIconRef.current.className = Style.loginButtonIconIdle;
        break;
    }
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter') {
      handleLogin();
    }
  }

  async function handleLogin() {
    loadingIconRef.current.disabled = true;
    loadingIconRef.current.className = Style.loginButtonLoading;
    setLoginText('');


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
          changeLoginAnimation('login');
          setUsername(usernameClient);
          navigate('/profile');
        }
        else {
          changeLoginAnimation('failed');
        }
      }).catch((error) => {
        console.error('Error logging in:', error);
      });

    if (usernameClient === '' || password === '') {
      return;
    }

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
