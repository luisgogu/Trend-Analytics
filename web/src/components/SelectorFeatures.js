import React,  {Component}  from 'react';
import Select from 'react-select';
import "./Selector.css"

const Features = [
   {label: "Material", value: 'material' },
   {label: "Color", value: 'color'} ,
   {label: "Room", value: 'room'} ,
   {label: "Style", value: 'style'} ,

];
var a = ""
var listFeatures = []
class App extends Component {
  state = {
    selectedOptions: [],
  }
  
  handleChange = (selectedOptions) => {
    this.setState({ selectedOptions });
    this.assignValue(selectedOptions);
    this.handleClick();
  }

  assignValue = (selectedOptions) => {
    a = selectedOptions.label
    //listFeatures = prod.filter(x => x.color === 'Red');
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
        "feature": a
      })
    })
  };
  // handleQuery = (selectedOptions) => {
  //   this.handleChange(selectedOptions);
  // }
  render() {
    const { selectedOptions } = this.state;
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-3"></div>
          <div className="col-md-6">
            <Select
              value={selectedOptions}
              options={Features}
              onChange={this.handleChange}/>
            
            {/* <ReactJson src={products} theme="monokai" /> */}
            
            
          </div>
        </div>
      </div>
    );
  }
}


export default App