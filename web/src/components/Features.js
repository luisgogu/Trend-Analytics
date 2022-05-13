import React,  {Component}  from 'react';
import Select from 'react-select';
//import 'bootstrap/dist/css/bootstrap.min.css';

const Countries = [
   {label: "material", value: 'material' },
   {label: "color", value: 'color'} ,
   {label: "size", value: 'size'} ,
   {label: "product", value: 'product'}
];
var a = ""
class App extends Component {
  state = {
    selectedOptions: [],
  }
  handleChange = (selectedOptions) => {
    this.setState({ selectedOptions });
  }
  handleClick = () => {
    fetch('http://127.0.0.1:5000/features',{
      credentials: 'include',
      method: 'POST',
      headers: {
      'Content-Type':'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST'},
      mode: 'no-cors',
      body: JSON.stringify({
        //"from": a[0],
        // "to":a[1],
        "feature": a//[2]
        })
    })
  };
  render() {
    const { selectedOptions } = this.state;
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-3"></div>
          <div className="col-md-6">
            <Select
              value={selectedOptions}
              options={Countries}
              onChange={this.handleChange}/>
              {a = selectedOptions.label}
              <button onClick={this.handleClick} className="btn-filter"> Filter </button>
          </div>
          <div className="col-md-4"></div>
        </div>
      </div>
    );
  }
}


export default App