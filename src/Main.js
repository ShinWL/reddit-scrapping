import React from 'react';
import Table from 'rc-table';
import 'rc-table/assets/index.css';
import {connect} from 'react-redux';

const columns = [
  {
    title: 'Posts',
    dataIndex: 'a',
    key: 'a',
    width: 50,
    align: 'left',
  },
  {
    title: 'User',
    dataIndex: 'b',
    key: 'b',
    width: 50,
    align: 'left',
  },
  {
    title: 'Comment',
    dataIndex: 'c',
    key: 'c',
    width: 50,
    align: 'left',
  },
];

class Main extends React.Component {

  render() {
    let data = [];
    for (let i = 0; i < this.props.posts.length; i++) {
      const post = this.props.posts[i];
      const comments = this.props.comments;
      let children = [];
      for (let j = 0; j < comments.length; j++) {
        if (comments[j].post === post.id)
          children.push(
              {
                a: comments[j].user_name + ' ' + comments[j].comment_content
              });
      }
      data = [
        ...data,
        {
          a: post.post_title,
          key: i,
          children: children,
        },
      ];
    }
    return (
        this.props.isLoaded ?
            <div align="center">
              <Table
                  data={data}
                  columns={columns}
                  style={{width: 500, text_align: 'justify'}}
                  rowKey={record => record.a}
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