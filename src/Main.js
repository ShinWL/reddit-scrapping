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
  handleOnEnterToLoad(e) {
    const baseURL = 'http://127.0.0.1:8000/api/';
    let input = this.refs.input;
    if (input.value) {
      if (e.keyCode === 13) {
        const postURL = baseURL + 'fetch_post/?subreddit=' +
            input.value + '&page=';
        // 100 pages
        for (let i = 1; i <= 2; i++) {
          console.log('Loading page: '+i)
          fetch(postURL + '' + i)
              .then(resp => {
                console.log('Page ' + i + ' Loaded.');
                return resp.json();
              })
              .then(data => {
                const commentURL = baseURL + 'fetch_comments/?post=';
                for (let j = 0; j < data.length; j++) {
                  fetch(commentURL + data[j].post_url)
                      .then(() => console.log(
                          'Done ' + j + ': '+ commentURL + data[j].post_url))
                }
              })
              // .then(()=> console.log('ALL DONE'));
        }

      }
    }
  }

  render() {
    // let data = [];
    // for (let i = 0; i < this.props.posts.length; i++) {
    //   const post = this.props.posts[i];
    //   const comments = this.props.comments;
    //   let children = [];
    //   for (let j = 0; j < comments.length; j++) {
    //     if (comments[j].post === post.id)
    //       children.push(
    //           {
    //             a: comments[j].user_name + ' ' + comments[j].comment_content
    //           });
    //   }
    //   data = [
    //     ...data,
    //     {
    //       a: post.post_title,
    //       key: i,
    //       children: children,
    //     },
    //   ];
    // }
    return (
        <div>
          <input type="search"
                 ref={'input'}
                 onKeyUp={this.handleOnEnterToLoad.bind(this)}
                 placeholder="Subreddit.."/>
        </div>

        // this.props.isLoaded ?
        //     <div align="center">
        //       {/*<Table*/}
        //           {/*data={data}*/}
        //           {/*columns={columns}*/}
        //           {/*style={{width: 500, text_align: 'justify'}}*/}
        //           {/*rowKey={record => record.a}*/}
        //       {/*/>*/}
        //     </div> : 'Loading'
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