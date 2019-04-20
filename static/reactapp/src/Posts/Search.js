import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import '../App.css'
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';


class Search extends Component {
    constructor(props){
        super(props)
        this.searchquery=this.searchquery.bind(this)
        this.handleChange = this.handleChange.bind(this)
        this.state={
          titlechecked:true,
          bodychecked:true
        }
    }

    searchquery()
    {
        const {searchdata} = this.props
        if(document.getElementById('search') !== null)
        {
            searchdata(document.getElementById('search').value,this.state.titlechecked,this.state.bodychecked)
        }
    
    }
    handleChange(event){
      let value = event.currentTarget.value
      let current = event.currentTarget.checked
      let checked 
      if (value === 'searchtitle' ){
        checked = this.state.titlechecked
        if(current === false && this.state.bodychecked === false)
        this.setState({
        titlechecked: checked
        })
        else 
        this.setState({
          titlechecked: !checked
          })
      }
      if (value === 'searchbody'){
        checked = this.state.bodychecked
        if(current === false && this.state.titlechecked === false)
        this.setState({
        bodychecked: checked
        })
        else 
        this.setState({
          bodychecked: !checked
          })
      }
    } 
  render() {
      
    return (
        <div >
        <form onSubmit={this.searchquery} > 
        <Paper elevation={3}>
        <InputBase className='searchInput' placeholder="Search" id='search' />
        <IconButton className='searchButton' aria-label="Search" onClick={this.searchquery}>
        <SearchIcon />
        </IconButton>
        </Paper>
        <FormGroup row>
        <FormControlLabel
          control={
            <Checkbox
              checked={this.state.titlechecked}
              onChange={this.handleChange}
              value="searchtitle"
            />
          }
          label="Title"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={this.state.bodychecked}
              onChange={this.handleChange}
              value="searchbody"
            />
          }
          label="body"
        />
        </FormGroup>
        </form>
       
        </div>
    );
  }
}

export default Search;
