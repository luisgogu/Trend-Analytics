import React from 'react'
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

function HeroSection() {
  return (
    <div className='hero-container'>
        <video src="/videos/video-3.mp4" loop autoPlay muted> </video>
        <h1>EXTRACTING TRENDS FROM SOCIAL NETWORKS</h1>
        <p>What are you waiting for</p>
        <div className='hero-btns'>
            <Button className='btns' buttonStyle = 'btn--outline' buttonSize = 'btn--large'>
                GET ANALYTICS
            </Button>
            <Button className='btns' buttonStyle = 'btn--primary' buttonSize = 'btn--large'>
                WATCH VIDEO <i className='far fa-play-circle'/>
            </Button>
        </div>
    </div>
  )
}

export default HeroSection