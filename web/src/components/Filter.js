import React, { useState } from "react";
import Graphics from './Graphics';
import SelectorFeatures from './SelectorFeatures';
import SelectorProducts from './SelectorProducts';
import './Filter.css'
import ranking from "./feature_list.json"


const Features = ranking;
const ShowAndHide = () => {
    const professions = ["Trending products", "Trending features"];
    const [myProfession, setMyProfession] = useState("");
    return (
        <div className="backpage">
            <div className="container">
                <div className="title-text">
                <img
                    className='logo_kave'
                    src={"../../images/feat.png"}
                    width={400}
                />
                    {/* <h2>Select the ranking you would like to see</h2> */}
                    <br />
                    <div
                        className="btn-group"
                    >
                        {professions.map(profession => (
                            <button
                                type="button"
                                key={profession}
                                className={"btn--prod"}
                                onClick={() => setMyProfession(profession)}
                            >
                                {profession.toLocaleUpperCase()}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="product">
                    
                    <>{myProfession}</>

                    <div className="back">
                        {myProfession === "Trending products" && (
                           <Graphics/> 
                        )}
                        {myProfession === "Trending features" && (
                            <div>
                                 <SelectorProducts/>
                                 <SelectorFeatures/>
                                <ul>{Features["Feature"].map(f => <li>{f}</li>)}</ul>
                            </div>
                        )}
                        
                    </div>
                </div>
            </div>
        </div>
    );
};



export default ShowAndHide;