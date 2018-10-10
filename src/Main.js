import React from 'react';
import Table from 'rc-table';
import 'rc-table/assets/index.css';
import {connect} from 'react-redux';

const columns = [{title: 'Posts', dataIndex: 'a', key: 'a', width: 50, align: 'left'}];

class Main extends React.Component {

  render() {

    return (
        this.props.isLoaded ?
            <div align="center">
              <Table
                  columns={columns}
                  style={{width: 500, text_align: 'justify'}}
              />
            </div> : 'Loading'
    );
  }
}

const mapStateToProps = (state) => {
  return ({
    posts: state.posts,
    comments: state.comments,
    isLoaded: state.isLoaded,
  });
};

export default connect(mapStateToProps)(Main);