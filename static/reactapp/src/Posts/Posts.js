import React, { Component } from 'react';
import '../App.css'
import 'whatwg-fetch'
import Details from './Details.js'
import Search from './Search.js'
import Switch from '@material-ui/core/Switch';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import Grid from '@material-ui/core/Grid';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from "@material-ui/core/CircularProgress";
import Fab from "@material-ui/core/Fab";


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
    let order = event.currentTarget.value
    this.setState({
      ordering: order
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
    if (!sortDsc) { endpoint = 'http://localhost:8000/api/article/?ordering=' + '-' + this.state.ordering }
    else {
      endpoint = 'http://localhost:8000/api/article/?ordering=' + this.state.ordering
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
              justify="center"
            >
              <Grid item className='searchArea'>
                <Search searchdata={this.filterposts} />
              </Grid>
              <Grid item className='filterButtons'>
                <FormControl component="fieldset" className='filterButtons' >
                  <RadioGroup
                    name="ordering"
                    value={this.state.ordering}
                    onChange={this.changeOrder}
                    row
                    id="orderingvalue"
                  >
                    <FormControlLabel value="author" control={<Radio color="primary" />} label="author" labelPlacement="start" />
                    <FormControlLabel value="title" control={<Radio color="primary" />} label="title" labelPlacement="start" />
                    <FormControlLabel value="pub_date" control={<Radio color="primary" />} label="public date" labelPlacement="start" />
                  </RadioGroup>
                </FormControl>
                <div align='right'>Asc <Switch value="checkedC" onChange={this.invertOrder} /> Desc</div>
              </Grid>
            </Grid>
            <Grid
              container justify="center" spacing={24}>
               {previous ?
                <Grid
                  item
                >

                  <Fab onClick={() => this.fetchPosts(previous)}
                    variant="extended" aria-label="Add" >
                    &lt;&lt; Previous
          </Fab>
                </Grid>
                : null}
              {next ?
                <Grid
                  item
                >
                  <Fab onClick={() => this.fetchPosts(next)}
                    variant="extended" aria-label="Add" >
                    Next >>
          </Fab>
                </Grid>
                : null}
            </Grid>
            {posts.length > 0 ? posts.map((postItem, index) => {
              return (
                <Details post={postItem} />
              )

            }) :
              <div align="center">
                <CircularProgress
                  variant="determinate"
                  value={this.state.completed}
                />
              </div>
            }

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
