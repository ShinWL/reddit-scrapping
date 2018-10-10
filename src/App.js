import React, {Component} from 'react';
import './App.css';
import connect from 'react-redux/es/connect/connect';
import {storeComments, storePosts, toggleIsLoaded} from './actions';
import Main from './Main';

class App extends Component {
  rootURL = 'http://127.0.0.1:8000/';

  componentDidMount() {
    fetch(this.rootURL + 'api/Posts')
        .then(resp => resp.json())
        .then(data => {
          this.props.dispatch(storePosts(data));
          this.props.dispatch(toggleIsLoaded(true));
        });
    fetch(this.rootURL + 'api/Comments')
        .then(resp => resp.json())
        .then(data => {
          this.props.dispatch(storeComments(data));
          this.props.dispatch(toggleIsLoaded(true));
        });
  }

  render() {
    console.log(this.props.posts);
    console.log(this.props.comments);
    return (
        <Main/>
    );
  }
}

const mapStateToProps = (state) => {
  return ({
    posts: state.posts,
    comments: state.comments,
  });
};

export default connect(mapStateToProps)(App);
