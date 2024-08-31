import React from 'react';
import NavbarStyle from '../Styles/Navbar.module.css';

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
                <button className={NavbarStyle.navbarButton}>Home</button>
                <button className={NavbarStyle.navbarButton}>About</button>
                <button className={NavbarStyle.navbarButton}>Contact</button>
            </div>

        </div>
    );
};

export default Navbar;