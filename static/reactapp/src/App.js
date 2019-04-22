import "@babel/polyfill/noConflict"
import React, { Component } from 'react';
import {render} from 'react-dom'
import './App.css';
import Posts from './Posts/Posts.js'
class App extends Component {
  render() {
    return (
      <div className="root">
      <Posts />
      </div>
    );
  }
}
render(<App/>,document.getElementById("root"))

export default App;
