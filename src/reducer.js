export const reducer = (state = {}, action) => {
  switch (action.type) {
    case 'STORE_POSTS':
      return {
        ...state,
        posts: action.payload,
      };
    case 'STORE_COMMENTS':
      return {
        ...state,
        comments: action.payload,
      };
    case 'TOGGLE_IS_LOADED':
      return {
        ...state,
        isLoaded: action.payload,
      };
    default:
      return state
  }
};