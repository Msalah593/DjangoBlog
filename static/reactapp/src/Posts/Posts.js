import React, { Component } from 'react';
import '../App.css'
import 'whatwg-fetch'
import Details from './Details.js'
import Search from './Search.js'
import Switch from '@material-ui/core/Switch';
import FormControl from '@material-ui/core/FormControl';
import Grid from '@material-ui/core/Grid';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from "@material-ui/core/CircularProgress";
import Button from "@material-ui/core/Button";
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';

const styles = theme => ({
  layout: {
    width: 'auto',
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(1100 + theme.spacing.unit * 3 * 2)]: {
      width: 1100,
      marginLeft: 'auto',
      marginRight: 'auto',
      align: 'center'
    },
  }
});

class Posts extends Component {
  constructor(props) {
    super(props)
    this.filterposts = this.filterposts.bind(this)
    this.loadPosts = this.loadPosts.bind(this)
    this.changeOrder = this.changeOrder.bind(this)
    this.invertOrder = this.invertOrder.bind(this)
    this.fetchPosts = this.fetchPosts.bind(this)
    this.state = {
      posts: [],
      search: null,
      searchtitle: true,
      searchbody: true,
      sortDsc: true,
      ordering: 'pub_date',
      completed: 0,
      next: null,
      previous: null
    }
  }

  progress = () => {
    const { completed } = this.state
    this.setState({ completed: completed >= 100 ? 0 : completed + 1 })
  }

  changeOrder(event) {
    console.log(event.target.name)
    this.setState({
      [event.target.name]: event.target.value
    }, () => {
      this.loadPosts()
    })
  }
  invertOrder(event) {
    let currentDsc = this.state.sortDsc
    this.setState({
      sortDsc: !currentDsc
    }, () => {
      this.loadPosts()
    })
    console.log(this.state.sortDsc)
  }
  filterposts(search, title, body) {
    console.log(search)
    this.setState({
      search: search,
      searchtitle: title,
      searchbody: body
    }, () => {
      this.loadPosts(search)
    })
  }
  loadPosts(search) {


    search = this.state.search
    let { sortDsc } = this.state
    let { searchtitle } = this.state
    let { searchbody } = this.state
    let endpoint
    if (!sortDsc) { endpoint = 'http://localhost:8000/api/article/?limit=20&ordering=' + '-' + this.state.ordering }
    else {
      endpoint = 'http://localhost:8000/api/article/?limit=20&ordering=' + this.state.ordering
    }
    if (search !== null && search !== undefined) { endpoint += '&search=' + search }
    if (searchtitle === true && searchbody === false) {
      endpoint += '&title_only=true'
    }
    else if (searchbody === true && searchtitle === false) {
      endpoint += '&body_only=true'
    }

    this.fetchPosts(endpoint)

  }

  fetchPosts(endpoint) {
    let thisComp = this
    let lookUpOptions = {
      method: "GET",
      headers: {
        'Content-Type': 'application/json'
      }
    }

    fetch(endpoint, lookUpOptions)
      .then(function (response) {
        return response.json()
      }).then(function (responseData) {
        thisComp.setState({
          posts: responseData.results,
          next: responseData.next,
          previous: responseData.previous
        })
      }).catch(function (error) {
        // console.log("error",error)
      })

  }
  componentDidMount() {

    this.loadPosts()
    this.timer = setInterval(this.progress, 20);

  }
  render() {
    const { posts } = this.state
    const { classes } = this.props
    const { next } = this.state
    const { previous } = this.state

    return (

      <React.Fragment>
        <div className={classes.layout}>
          <Grid container spacing={40} alignItems="center"
            justify="center">
            <Grid
              container
              justify="center" >
              <Grid item className='searchArea'>
                <Search searchdata={this.filterposts} >
                <Grid container className="sortBy">
              <FormControl component="fieldset"  >
          <Select
            value={this.state.ordering}
            onChange={this.changeOrder}
            id="orderingvalue"
            name="ordering"
          >
            <MenuItem value="author">author</MenuItem>
            <MenuItem value="title">title</MenuItem>
            <MenuItem value="pub_date">pub_date</MenuItem>
          </Select>
        </FormControl>
                <div align='right'>Asc <Switch value="checkedC" onChange={this.invertOrder} /> Desc</div>
              
            </Grid>
                </Search>
              </Grid>
              </Grid>
            {posts.length > 0 ? posts.map((postItem, index) => {
              return (
                <Details key={index} post={postItem} />
              )

            }) :
              <div align="center">
                <CircularProgress
                  variant="determinate"
                  value={this.state.completed}
                />
              </div>
            }
          
          <Grid
              container justify="center" spacing={24} className="pagination">
               {previous ?
                <Grid
                  item
                >

                  <Button onClick={() => this.fetchPosts(previous)}
                    variant="outlined" aria-label="Add" >
                    &lt;&lt; Previous
          </Button>
                </Grid>
                : null}
              {next ?
                <Grid
                  item
                >
                  <Button onClick={() => this.fetchPosts(next)}
                    variant="outlined" aria-label="Add" >
                    Next >>
          </Button>
                </Grid>
                : null}
            </Grid>

          </Grid>
        </div>
      </React.Fragment>

    );
  }
}

Posts.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Posts);
