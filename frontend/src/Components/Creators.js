import React from 'react';
import ExplenationStyle from '../Styles/ExplenationStyle.module.css';
import CreatorsStyle from '../Styles/CreatorsStyle.module.css';
import PageDesign from '../Styles/PageDesign.module.css';
import { Link } from 'react-router-dom';
import { FaGithub } from "react-icons/fa6";


function Contact() {
    return (
        <>
            <div className={PageDesign.mainDiv}>
                <h1>Nice to meet you!</h1>
                <p>We are Maxim and Dima.</p>
                <div className={CreatorsStyle.wrapper}>
                    <div className={CreatorsStyle.explanationDiv}>
                        <img className={ExplenationStyle.image} src="Maxim.jpg" alt="Maxim" style={{ maxWidth: "300px" }} />
                        <h2 style={{ marginBottom: "0", marginTop: "0" }}>Maxim Lebedinsky</h2>
                        <p style={{ marginBottom: "20px" }}>Created the video model, and developed most of the backend side for this website.</p>
                        <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                            <div>
                                <FaGithub />
                                <Link to="https://github.com/MaximL98" style={{ marginLeft: "10px" }}>MaximL98</Link>
                            </div>

                        </div>
                    </div>
                    <div className={CreatorsStyle.explanationDiv}>
                        <img className={ExplenationStyle.image} src="Dima.png" alt="Dima" style={{ maxWidth: "300px" }} />
                        <h2 style={{ marginBottom: "0", marginTop: "0" }}>Dima Kislitsyn</h2>
                        <p style={{ marginBottom: "20px" }}>Created the audio model, and developed most of the frontend side of this website.</p>
                        <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                            <div>
                                <FaGithub />
                                <Link to="https://github.com/DimaKyn" style={{ marginLeft: "10px" }}>DimaKyn</Link>
                            </div>

                        </div>
                    </div>
                </div>


            </div>
        </>
    )
}

export default Contact;