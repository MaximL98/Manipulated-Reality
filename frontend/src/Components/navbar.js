import React, { useEffect, useRef, useState } from 'react';
import NavbarStyle from '../Styles/Navbar.module.css';
import { FaUserAlt } from "react-icons/fa";
import { Link, useNavigate } from 'react-router-dom';

import { AuthContext } from './AuthProvider';
import { useContext } from 'react';



const Navbar = () => {
    const { username, setUsername } = useContext(AuthContext);
    const navigate = useNavigate();
    const profileMenuRef = useRef(null);
    const [loggedInUser, setLoggedInUser] = useState(username);
    
    function handleButtonClick() {
    }

    function handleLogout() {
        setLoggedInUser(null);
        setUsername("");
        navigate("/");
    }

    function handleMenuClick() {
        profileMenuRef.current.classList.toggle(NavbarStyle.activeProfileMenu);
        console.log("clicked");
    }

    useEffect(() => {
        if (username) {
            setLoggedInUser(true);
        }
    }, [username]);
    return (
        <div className={NavbarStyle.navBar}>
            <div className={NavbarStyle.logoWrapper}>
                <div className={NavbarStyle.mrLogo}>
                    <div className={NavbarStyle.innerLogoDiv}>
                        <img src="ManipulatedRealityLogo_MR.png" alt="Manipulated Reality Logo" className={NavbarStyle.logoImage} />
                    </div>

                </div> </div>

            <div className={NavbarStyle.navbarButtonDiv}>
                <Link to="/"><button className={NavbarStyle.navbarButton}>Home</button></Link>
                <Link to="/About"><button className={NavbarStyle.navbarButton}>About</button></Link>
                <Link to="/Contact"><button className={NavbarStyle.navbarButton}>Contact</button></Link>
                <Link to="/Upload_file"><button className={NavbarStyle.navbarButton}>Upload file</button></Link>

            </div>



            <div className={NavbarStyle.profileIconDiv} onClick={() => handleMenuClick()}>
                <FaUserAlt className={NavbarStyle.profileIcon} />

            </div>

            <div ref={profileMenuRef} className={NavbarStyle.profileIconMenu} >


                <div className={NavbarStyle.profileIconButtonContainer}>
                    {loggedInUser ? (
                        <>
                            <div style={{ fontSize: "15px", fontWeight: "bold", paddingBottom: "5px", marginTop: "-10px" }}>
                                {username.charAt(0).toUpperCase() + username.slice(1)}
                            </div>
                            <Link onClick={() => handleButtonClick()} to="/profile" className={NavbarStyle.profileIconButton}>MY PROFILE</Link>
                            <button onClick={handleLogout} className={NavbarStyle.logoutButton} style={{ marginTop: "10px" }}>LOGOUT</button>
                        </>
                    ) : (
                        <>
                            <Link onClick={() => handleButtonClick()} to="/login" className={NavbarStyle.profileIconButton}>LOGIN</Link>
                            <Link onClick={() => handleButtonClick()} to="/register" className={NavbarStyle.profileIconButton} style={{ marginTop: "10px" }}>REGISTER</Link>
                        </>
                    )}
                </div>
            </div >

        </div>
    );
};

export default Navbar;