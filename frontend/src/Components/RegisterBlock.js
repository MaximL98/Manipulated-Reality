import Style from '../Styles/LoginBlock.module.css';
import { FaUserAlt, FaKey } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import React, { useState, useEffect, useRef } from 'react';
import { BiLoader } from 'react-icons/bi';
import { MdOutlineEmail } from "react-icons/md";
import { AuthContext } from './AuthProvider';
import { useContext } from 'react';

function RegisterBlock() {
    const { setUsername, setToken, username, token } = useContext(AuthContext);

    const [email, setEmail] = useState('');
    const [usernameClient, setUsernameClient] = useState('');
    const [password, setPassword] = useState('');
    const registerButtonRef = useRef(null);
    const incorrectCredentialsLabelRef = useRef(null);
    const [registerText, setRegisterText] = useState('Register');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const loadingIconRef = useRef(null);
    const navigate = useNavigate();

    function changeRegisterAnimation(status) {
        switch (status) {
            case 'register':
                loadingIconRef.current.className = Style.loginButtonIconIdle;
                registerButtonRef.current.disabled = true;
                registerButtonRef.current.style.className = Style.loginButton;
                registerButtonRef.current.style.borderColor = 'green';
                registerButtonRef.current.style.color = 'rgb(144, 238, 144)';
                incorrectCredentialsLabelRef.current.disabled = true;
                setRegisterText('Success!');
                break;
            case 'failed':
                registerButtonRef.current.className = Style.loginButton;
                registerButtonRef.current.disabled = false;
                loadingIconRef.current.className = Style.loginButtonIconIdle;
                incorrectCredentialsLabelRef.current.disabled = false;
                incorrectCredentialsLabelRef.current.className = Style.incorrectCredentialsLabelShow;
                setRegisterText('Register');
                break;
            default:
                registerButtonRef.current.disabled = false;
                loadingIconRef.current.className = Style.loginButtonIconIdle;
                break;
        }
    }


    function handleKeyPress(e) {
        if (e.key === 'Enter') {
            handleRegister();
        }
    }

    async function handleRegister() {
        loadingIconRef.current.disabled = true;
        loadingIconRef.current.className = Style.loginButtonIconLoading;
        setRegisterText('');

        const form = new FormData();
        form.append('username', usernameClient);
        form.append('password', password);
        form.append('email', email);

        await fetch('/register', {
            method: 'POST',
            body: form
        })
            .then((response) => response.json())
            .then(jsonData => {
                if (jsonData === "USER REGISTERED") {
                    changeRegisterAnimation('register');
                    setUsername(usernameClient);
                    navigate('/profile');
                }
                else {
                    changeRegisterAnimation('failed');
                }
            }).catch((error) => {
                console.error('Error logging in:', error);
            });

        if (usernameClient === '' || password === '' || email === '') {
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
                <label className={Style.loginLabel}>Register</label>
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
                    <label className={Style.usernameLabel}>Username</label>
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
                <div className={Style.emailBlock}>
                    <MdOutlineEmail className={Style.userIcon} />
                    <input
                        required
                        pattern=".*\S.*"
                        type="text"
                        className={Style.emailInput}
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        onKeyDown={handleKeyPress}
                    />
                    <label className={Style.emailLabel}>Email</label>
                </div>
                <div className={Style.buttonDiv}>
                    <button
                        ref={registerButtonRef}
                        className={Style.loginButton}
                        onClick={handleRegister}
                    >
                        <div ref={loadingIconRef} className={Style.loginButtonIconIdle}>
                            <BiLoader />
                        </div>
                        {registerText}
                    </button>
                    <label ref={incorrectCredentialsLabelRef} className={Style.incorrectCredentialsLabel}>
                        User already exists!
                    </label>
                    <label style={{ fontSize: '20px', color: "rgba(80, 80, 250, 1)" }}>
                        New to Manipulated Reality?
                    </label>
                    <Link to="/Login" className={Style.registerButton}>
                        Login now
                    </Link>
                </div>
            </div>
        </>
    );
}

export default RegisterBlock;
