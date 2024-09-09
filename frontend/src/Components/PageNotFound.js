import { Link } from "react-router-dom";
import PageDesign from "../Styles/PageDesign.module.css";
import ExplenationDesign from "../Styles/ExplenationStyle.module.css";
import MainPage from "../Styles/MainPage.module.css";

function PageNotFound() {
    return (
        <div className={PageDesign.mainDiv}>
            <div className={ExplenationDesign.explenationDiv}>
                <h1>404</h1>
                <h2>Page Not Found</h2>
                <Link to="/"><button className={MainPage.uploadButton}>Go home</button></Link>
            </div>
        </div>
    )
}

export default PageNotFound;