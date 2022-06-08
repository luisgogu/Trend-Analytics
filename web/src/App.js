import React from 'react'
import Navbar from './components/Navbar'
import {BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './App.css';
import Home from './components/pages/Home';
import Results from './components/pages/Results';
import Video from './components/pages/Video';

function App() {
  return (
    <div className='container'>
    <Router>
      <Navbar />
      <Switch>
      <Route path='/' exact component = {Home} />
      <Route path='/results' exact component = {Results} />
      <Route path='/video' exact component = {Video} />
      </Switch>
    </Router>
      
    </div>
  );
}

export default App;