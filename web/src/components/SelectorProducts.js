import React,  {Component}  from 'react';
import Select from 'react-select';
import "./Selector.css"

//import 'bootstrap/dist/css/bootstrap.min.css';

const Products = [
   {label: "Sofa", value: 'all' },
   {label: "Chair", value: 'all' },
   {label: "Mat", value: 'all' },
   {label: "Shelves", value: 'all' },
   {label: "Jar", value: 'all' },
   {label: "Vase", value: 'all' },
   {label: "Lamp", value: 'all' },
   {label: "Frame", value: 'all' },
   {label: "Table", value: 'all' },
   {label: "Lampshade", value: 'all' },
   {label: "Wallpaper", value: 'all' },
   {label: "Coat racks", value: 'all' },
   
];
var a = ""
class App extends Component {
  state = {
    selectedOptions: [],
  }
  handleClick = () => {
    fetch('http://127.0.0.1:5000/prodfeatures',{
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
        "product": a//[2]
        })
    })
  };
  handleChange = (selectedOptions) => {
    this.setState({ selectedOptions });
    this.assignValue(selectedOptions);
    this.handleClick();
  }
  assignValue = (selectedOptions) => {
    if (selectedOptions.label !== "All"){
      a = selectedOptions.label
    } else {
      a = Products.label
    }
  }
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
              options={Products}
              onChange={this.handleChange}/>
              
              {/*<button onClick={this.handleClick} className="btn-filter"> Filter </button>*/}
          </div>
          <div className="col-md-4"></div>
        </div>
      </div>
    );
  }
}


export default App