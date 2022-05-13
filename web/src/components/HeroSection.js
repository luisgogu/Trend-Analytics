import React from 'react'
import '../App.css';
import { Button_results, Button_video } from './Button';
import './HeroSection.css';

function HeroSection() {
  return (
    <div className='hero-container'>
        <video src="/videos/video-3.mp4" autoPlay loop muted> </video>
        <h1>EXTRACTING TRENDS FROM SOCIAL NETWORKS</h1>
        <p>What are you waiting for</p>
        <div className='hero-btns'>
            <Button_results className='btns' buttonStyle = 'btn--primary' buttonSize = 'btn--large'>
                GET ANALYTICS
            </Button_results>
            <Button_video className='btns' buttonStyle = 'btn--outline' buttonSize = 'btn--large'>
                WATCH VIDEO <i className='far fa-play-circle'/>
            </Button_video>
        </div>
    </div>
  )
}

export default HeroSection