import {LOGIN} from '../actions/auth';

const defaultState = {
	isAuth: false,
	username: '',
	error: false,
	errorMessage: ''
};

const auth = (state = defaultState, action) => {
	switch (action.type) {
	  case LOGIN: {
		  const {username} = action;
		  
		  return {
			  ...state,
			  username,
			  isAuth: true
		  };
	  }
	  default:
		return state
	}
};

export default auth;