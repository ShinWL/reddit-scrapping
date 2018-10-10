export function storePosts(posts) {
  return ({
    type: 'STORE_POSTS',
    payload: posts,
  });
}

export function storeComments(comments) {
  return ({
    type: 'STORE_COMMENTS',
    payload: comments,
  });
}

export function toggleIsLoaded() {
  return ({
    type: 'TOGGLE_IS_LOADED',
    payload: true,
  });
}