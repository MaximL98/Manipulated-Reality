import { Link } from "react-router-dom";
import Style from "../Styles/Navbar.module.css";
import { GiHamburgerMenu } from "react-icons/gi";
import { CgClose } from "react-icons/cg";
import { useRef, useState, useEffect } from "react";
import { MdAccountCircle } from "react-icons/md";
import { BsFillPersonFill } from "react-icons/bs";
import { AiFillHome } from "react-icons/ai";
import { AiFillInfoCircle } from "react-icons/ai";
import { BsArrowUpShort } from "react-icons/bs";
import { AuthContext } from "./AuthProvider";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
    const { username, setUsername } = useContext(AuthContext);
    const navigate = useNavigate();
    const [loggedInUser, setLoggedInUser] = useState(username);

    function handleLogout() {
        setLoggedInUser(null);
        setUsername("");
        navigate("/");
    }

    useEffect(() => {
        if (username) {
            setLoggedInUser(true);
        }
    }, [username]);



    //Variables for the hamburger menu
    const [hamburgerMenuOpen, setHamburgerMenuOpen] = useState(false);
    const [hamburgerCloserHidden, setHamburgerCloserHidden] = useState(true);
    const hamburgerMenu = useRef(null);
    const navbar = useRef(null);
    const lowerOpacityHamburgerOpen = useRef(null);

    //Variables for the profile icon menu
    const profileMenu = useRef(null);
    const [profileMenuOpen, setProfileMenuOpen] = useState(false);

    //Hook to update isLoggedIn state
    useEffect(() => {
        if (loggedInUser) {
            setLoggedInUser(true);
        }
    }, []);

    //This function makes the hamburger menu close if you click outside the hamburger menu
    const handleLowerOpacityClick = () => {
        if (hamburgerMenuOpen) {
            handleHamburgerClick();
        }
        //Profile menu is open
        else {
            handleProfileIconClick();
        }
    };

    //This function handles the hamburger menu opening and closing
    //Upon click, changes the className of components
    const handleHamburgerClick = () => {
        if (profileMenuOpen && !hamburgerMenuOpen) {
            handleProfileIconClick();
        }
        //Change the boolean state of the hamburger menu
        setHamburgerMenuOpen(!hamburgerMenuOpen);
        setHamburgerCloserHidden(!hamburgerCloserHidden);
        if (hamburgerMenuOpen) {
            lowerOpacityHamburgerOpen.current.className = `${Style.lowerOpacityHamburgerOpen}`;
            hamburgerMenu.current.className = `${Style.hamburgerMenu} ${Style.hidden}`;
            navbar.current.className = `${Style.wrapper} ${Style.navHalfOpacity}`;
        }
        else {
            lowerOpacityHamburgerOpen.current.className = `${Style.lowerOpacityHamburgerOpen} ${Style.lowerOpacityActive}`;
            hamburgerMenu.current.className = `${Style.hamburgerMenu} ${Style.active}`;
            navbar.current.className = `${Style.wrapper} ${Style.navFullOpacity}`;
        }
    };

    //This function handles the profile icon menu opening and closing
    const handleProfileIconClick = () => {
        if (hamburgerMenuOpen && !profileMenuOpen) {
            handleHamburgerClick();
        }
        //Change the boolean state of the profile menu
        setProfileMenuOpen(!profileMenuOpen);
        if (profileMenuOpen) {
            lowerOpacityHamburgerOpen.current.className = `${Style.lowerOpacityHamburgerOpen}`;
            profileMenu.current.className = `${Style.profileIconMenu} `;
            navbar.current.className = `${Style.wrapper} ${Style.navHalfOpacity}`;
        }

        else {
            lowerOpacityHamburgerOpen.current.className = `${Style.lowerOpacityHamburgerOpen} ${Style.lowerOpacityActive}`;
            profileMenu.current.className = `${Style.profileIconMenu} ${Style.activeProfileMenu}`;
            navbar.current.className = `${Style.wrapper} ${Style.navFullOpacity}`;
        }
    };

    //If the hamburger menu is open and you click on a button, the hamburger menu closes
    const handleButtonClick = () => {
        if (hamburgerMenuOpen) {
            handleHamburgerClick();
        }
        if (profileMenuOpen) {
            handleProfileIconClick();
        }
    }

    return <>
        <div ref={lowerOpacityHamburgerOpen} className={Style.lowerOpacityHamburgerOpen}
            onClick={() => handleLowerOpacityClick()}></div>
        <div ref={navbar} className={Style.wrapper}>
            {/*Navbar*/}
            {!hamburgerMenuOpen && <GiHamburgerMenu className={Style.hamburger} onClick={() => handleHamburgerClick()} />}
            {!hamburgerCloserHidden &&
                <CgClose className={Style.hamburgerCloser} onClick={() => handleHamburgerClick()} />}
            <div className={Style.rightSide}>
                <div className={Style.logo}>
                    <div className={Style.logoContainer}>
                        <img src="ManipulatedRealityLogo_MR.png" className={Style.logoContainer}/>
                        <Link onClick={() => handleButtonClick()} style={{ height: "100%", width: "100%", cursor: "pointer", position: "absolute" }} to="/"></Link>
                    </div>
                </div>
            </div>
            <div className={Style.buttons} style={{ display: "flex", justifyContent: "space-between" }}>
                <MdAccountCircle style={{ fontSize: "45px", cursor: "pointer" }} onClick={() => handleProfileIconClick()} />
            </div>
        </div>

        {/*Profile Icon Menu*/}
        <div ref={profileMenu} className={Style.profileIconMenu} >


            <div className={Style.profileIconButtonContainer}>
                {loggedInUser ? (
                    <>
                        <div style={{ fontSize: "15px", fontWeight: "bold", paddingBottom: "5px", marginTop: "-10px", color: "white" }}>
                            Welcome back, {username.charAt(0).toUpperCase() + username.slice(1)}.
                        </div>
                        <Link onClick={() => handleButtonClick()} to="/profile" className={Style.profileIconButton}>MY PROFILE</Link>
                        <button onClick={() => handleLogout()} className={Style.logoutButton} style={{ marginTop: "10px" }}>LOGOUT</button>
                    </>
                ) : (
                    <>
                        <Link onClick={() => handleButtonClick()} to="/login" className={Style.profileIconButton}>LOGIN</Link>
                        <Link onClick={() => handleButtonClick()} to="/register" className={Style.profileIconButton} style={{ marginTop: "10px" }}>REGISTER</Link>
                    </>
                )}
            </div>
        </div >
        {/*Hamburger Menu*/}
        <div ref={hamburgerMenu} className={Style.hamburgerMenu}>
            <div className={Style.hamburgerButtons}>
                <div className={Style.topIcons}>
                    {/* Profile icon inside the hamburger menu*/}
                    <div className={Style.iconContainer}>
                        <Link onClick={() => handleButtonClick()} to="/">
                            <AiFillHome />
                        </Link>
                    </div>
                    <label style={{ width: "auto" }}>MENU</label>
                    {/* Home icon inside the hamburger menu*/}
                    {loggedInUser ? (
                        <div className={Style.iconContainer}>
                            <Link onClick={() => handleButtonClick()} to="/Profile">
                                <BsFillPersonFill />
                            </Link>

                        </div>
                    ) : (
                        <div className={Style.iconContainer}>
                            <Link onClick={() => handleButtonClick()} to="/Login">
                                <BsFillPersonFill />
                            </Link>

                        </div>
                    )}
                </div>


                {loggedInUser ? (
                    <div className={Style.hamburgerLinksContainer}>
                        <Link onClick={() => handleButtonClick()} to="/" className={Style.hamburgerLinks}>Home</Link>
                        <Link onClick={() => handleButtonClick()} to="/About" className={Style.hamburgerLinks}>About</Link>
                        <Link onClick={() => handleButtonClick()} to="/UploadFilePage" className={Style.hamburgerLinks}>Upload file</Link>
                    </div>
                ) : (
                    <div className={Style.hamburgerLinksContainer}>
                        <Link onClick={() => handleButtonClick()} to="/" className={Style.hamburgerLinks}>Home</Link>
                        <Link onClick={() => handleButtonClick()} to="/About" className={Style.hamburgerLinks}>About</Link>
                    </div>
                )}

                <div className={Style.bottomSection}>
                    <Link onClick={() => handleButtonClick()} to="/Creators">
                        <AiFillInfoCircle className={Style.infoCircle} />
                    </Link>
                </div>

            </div>
        </div>
    </>



}

export default Navbar;
