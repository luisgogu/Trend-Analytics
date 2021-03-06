import Checkbox from "./Checkbox";
//import logo from './logo.svg';
//import './App.css';
import React from 'react';
import "./Styles.css";
import DateRangeExample from "./DateRangeExample";
import Chart from "./Chart";
import "./Graphics.css"


var a = []
const OPTIONS = ["Rug","Pillow","Wardrobe","Seat","Tray","Bag","Armchair","Box","Drawer","Bed","Changing mat","Storage bed","Basket","Chaise longue","Cushion","Mattress","Hanger","Curtain","Picture","Ladder","Desk","Mirror","Shelf","Mat", "Shelves", "Jar", "Vase", "Lamp", "Frame", "Table", "Lampshade", "Wallpaper", "Coat racks", "Kids protector", "Puff", "Clock", "Footstool", "Chair", "Couch", "Sofa", "Stool", "Suction pad", "Shoerack"];
class App extends React.Component {
  state = {
    checkboxes: OPTIONS.reduce(
      (options, option) => ({
        ...options,
        [option]: false
      }),
      {}
    )
  };

  selectAllCheckboxes = isSelected => {
    Object.keys(this.state.checkboxes).forEach(checkbox => {
      // BONUS: Can you explain why we pass updater function to setState instead of an object?
      this.setState(prevState => ({
        checkboxes: {
          ...prevState.checkboxes,
          [checkbox]: isSelected
        }
      }));
    });
  };

  selectAll = () => this.selectAllCheckboxes(true);

  deselectAll = () => this.selectAllCheckboxes(false);

  handleCheckboxChange = changeEvent => {
    const { name } = changeEvent.target;

    this.setState(prevState => ({
      checkboxes: {
        ...prevState.checkboxes,
        [name]: !prevState.checkboxes[name]
      }
    }));
  };

  handleFormSubmit = formSubmitEvent => {
    formSubmitEvent.preventDefault();

    Object.keys(this.state.checkboxes)
      .filter(checkbox => this.state.checkboxes[checkbox])
      .forEach(checkbox => {
        a.push(checkbox);
    })
        fetch('http://127.0.0.1:5000/prod',{
          credentials: 'include',
          method: 'POST',
          headers: {
          'Content-Type':'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST'},
          mode: 'no-cors',
          body: JSON.stringify({
            //"from": a[0],
            //"to":a[1],
            "product":a
        })
      });
      this.deselectAll();
      a = [];
  };

  //handleClick = () => {
    // fetch('http://127.0.0.1:5000',{
    //   credentials: 'include',
    //   method: 'POST',
    //   headers: {
    //   'Content-Type':'application/json',
    //   'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Methods': 'POST'},
    //   mode: 'no-cors',
    //   body: JSON.stringify({
    //     //"from": a[0],
    //     // "to":a[1],
    //     "product":a//[2]
    //     })
    // })
    //a = []
  //};
  createCheckbox = option => (
    <Checkbox
      label={option}
      isSelected={this.state.checkboxes[option]}
      onCheckboxChange={this.handleCheckboxChange}
      key={option}
    />
  );

  createCheckboxes = () => OPTIONS.map(this.createCheckbox);

  
  render() {
    return (
      <div className="container">
        <div className="row mt-5">
          <div className="filter">
            <form onSubmit={this.handleFormSubmit}>
              <div>
                Filter by product category
              </div>
              {this.createCheckboxes()}

              <div className="form-group-mt-2">
                <button
                  type="button"
                  className="btn btn-outline-primary mr-2"
                  onClick={this.selectAll}
                >
                  Select All
                </button>
                <button
                  type="button"
                  className="btn btn-outline-primary mr-2"
                  onClick={this.deselectAll}
                >
                  Deselect All
                </button>
                
                  <DateRangeExample />
                <button type="submit" className="btn-filter" >
                  Filter
                </button>
              </div>
            </form>
          </div>
        </div>
        <div className="chart">
          <Chart/>
        </div>
      </div>
    );
  }
}

export default App;