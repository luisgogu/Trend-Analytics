import React, { useState } from "react";
import Graphics from './Graphics';
import Features from './Features';
import './Filter.css'


const ShowAndHide = () => {
    const professions = ["Trending products", "Trending features"];
    const [myProfession, setMyProfession] = useState("");
    return (
        <div className="backpage">
            <div className="container">
                <div className="title-text">
                    <h2>Select the ranking you would like to see</h2>
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
                    <p>{myProfession}</p>

                    <p>
                        {myProfession === "Trending products" && (
                           <Graphics/> 
                        )}
                        {myProfession === "Trending features" && (
                            <Features/> 
                        )}
                    </p>
                </div>
            </div>
        </div>
    );
};



export default ShowAndHide;