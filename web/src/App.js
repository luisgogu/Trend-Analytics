import React from 'react'
import Navbar from './components/Navbar'
import {BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './App.css';
import Home from './components/pages/Home';
import Results from './components/pages/Results';

function App() {
  return (
    <>
    <Router>
      <Navbar />
      <Switch>
      <Route path='/' exact component = {Home} />
      <Route path='/results' exact component = {Results} />
      </Switch>
    </Router>
      
    </>
  );
}

export default App;
