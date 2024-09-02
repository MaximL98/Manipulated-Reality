import React from 'react';
import NavbarStyle from '../Styles/Navbar.module.css';
import { FaUserAlt } from "react-icons/fa";
import { Link } from 'react-router-dom';


const Navbar = () => {
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
            </div>

            <div className={NavbarStyle.profileIconDiv}>
                <FaUserAlt className={NavbarStyle.profileIcon} />
            </div>

        </div>
    );
};

export default Navbar;