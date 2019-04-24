import React, { Component } from 'react';
import '../App.css'
import Typography from '@material-ui/core/Typography'
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Hidden from '@material-ui/core/Hidden';



const styles = theme => ({
  layout: {
    width: 'auto',
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(1100 + theme.spacing.unit * 3 * 2)]: {
      width: 1100,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  card: {
    display: 'flex',
  },
  cardDetails: {
    flex: 1,
  },
  cardMedia: {
    width: 160,
  },
});

class App extends Component {

  constructor(props) {
    super(props)
    this.setPostStateOnProps = this.setPostStateOnProps.bind(this)
    this.formateDate = this.formateDate.bind(this)
    this.state = {
      postItem: ''
    }
  }
  
  formateDate(unformatteddate){
    var months = [
      "Jan.","Feb.","Mar.","April","May","June","July","Aug.","Sept.","Oct.","Nov.","Dec."
    ]
    var date = new Date(unformatteddate)
    var formatteddate = months[date.getMonth()]
    formatteddate += " " + date.getDay() + "," + date.getFullYear() + ","
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var time = (hours > 11 ? (hours - 11) : (hours + 1)) + ":" + minutes + (hours > 11 ? "pm." : "pm.");
    return formatteddate + " " + time
  }

  setPostStateOnProps() {
    const { post } = this.props
    this.setState({
      postItem: post
    })

  }
  componentDidMount() {
    this.setPostStateOnProps()
  }
  componentDidUpdate(prevProps, prevState, snapshop) {
    if (this.props !== prevProps) {
      this.setPostStateOnProps()
    }
  }
  render() {
    const { postItem } = this.state
    const { classes } = this.props
    return (
     
      <React.Fragment>
            {
              <Grid item key={postItem.title} xs={12} md={6} >
                {/* <a   Style="text-decoration:none;"> */}
                <Card 
                onClick={()=> window.top.location.href = "http://localhost:8000/articles/" + postItem.id } 
                className={classes.card}>
                  <div className={classes.cardDetails}>
                    <CardContent>
                      <Typography component="h2" variant="h5">
                        {postItem.title}
                      </Typography>
                      <Typography variant="subtitle1" color="textSecondary">
                        {this.formateDate(postItem.pub_date)}
                      </Typography>
                      <Typography className="textwrap" variant="subtitle1" paragraph>
                        {postItem.body}
                      </Typography>
                      <Typography variant="subtitle1" color="primary">
                      Posted by {postItem.author_username}
                      </Typography>
                    </CardContent>
                  </div>
                  <Hidden xsDown>
                    <CardMedia
                      className={classes.cardMedia}
                      image="data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22288%22%20height%3D%22225%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20288%20225%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_164edaf95ee%20text%20%7B%20fill%3A%23eceeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_164edaf95ee%22%3E%3Crect%20width%3D%22288%22%20height%3D%22225%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%2296.32500076293945%22%20y%3D%22118.8%22%3EThumbnail%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E" // eslint-disable-line max-len
                      title="Image title"
                    />
                  </Hidden>
                </Card>
                {/* </a> */}
              </Grid>
            }
    </React.Fragment>

    );
  }
}

App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);
