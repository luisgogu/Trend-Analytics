import React from "react";
import DateRangePicker from "react-daterange-picker";
import "react-daterange-picker/dist/css/react-calendar.css";
import originalMoment from "moment";
import { extendMoment } from "moment-range";
const moment = extendMoment(originalMoment);

var a = [[],[]]
class Example extends React.Component {
  constructor(props, context) {
    super(props, context);

    const today = moment();

    this.state = {
      isOpen: true,
      value: moment.range(today.clone().subtract(7, "days"), today.clone())
    };
  }

  onSelect = (value, states) => {
      a[0].push(value.start.format('YYYY-MM-DD'));
      a[1].push(value.end.format('YYYY-MM-DD'));
    
      fetch('http://127.0.0.1:5000/date',{
            credentials: 'include',
            method: 'POST',
            headers: {
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST'},
            mode: 'no-cors',
            body: JSON.stringify({
              "from": a[0],
              "to":a[1],
              //"product":a[2]
          })
      });
    a = [[],[]]
    this.setState({ value, states });
  };

  onToggle = () => {
    this.setState({ isOpen: !this.state.isOpen });
  };

  renderSelectionValue = () => {
    return (
      <div>
        <div>Filter by date</div>
        {"From "}
        {this.state.value.start.format("YYYY/MM/DD")}
        {" to "}
        {this.state.value.end.format("YYYY/MM/DD")}
      </div>
    );
  };

  render() {
    return (
      <div>
        <div>{this.renderSelectionValue()}</div>

        <div>
          <form
            onClick={this.onToggle}
          />
        </div>

        {this.state.isOpen && (
          <DateRangePicker
            value={this.state.value}
            onSelect={this.onSelect}
            singleDateRange={true}
          />
        )}
      </div>
    );
  }
}

export default Example;