//import logo from './logo.svg';
//import './App.css';
import React from 'react';
import data from "./data.json";
import { PieChart, Pie, Sector, ResponsiveContainer } from 'recharts';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import "./Graphics.css"

class Graph extends React.Component {
state = {
  data: data.products,
  activeIndex: 0,
};

handleClick = (data, index) => {
  this.setState({
    activeIndex: index,
  });
};
render() {
  const { activeIndex, data } = this.state;
  const activeItem = data[activeIndex];

  return (
    <div className='container'>
    <p>Click each rectangle </p>
    <div className='row'>
    <ResponsiveContainer width="100%" aspect={3}>
      <BarChart width={150} aspect={3} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="product" />
          <Tooltip />
        <Bar dataKey="popularity" onClick={this.handleClick}>
          {data.map((entry, index) => {
            return (
              <Cell cursor="pointer" fill={index === activeIndex ? '#c65653' : '#808080'} key={`cell-${index}`} />
            );
          })}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
    </div>
    
    <img className='image' src={activeItem.url} width={400}/>
    <p className="content">{<img src={this.state.url} aspectRatio={1.5}/>}</p>
  </div>
  );
}
}
export default Graph;