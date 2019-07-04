import { SET_WIKI_LANGUAGE } from '../actions/app'

const defaultState = {
	wiki: 'lv'
};

const app = (state = defaultState, action) => {
	switch (action.type) {
	  case SET_WIKI_LANGUAGE: {
		  const {language} = action;
		  
		  return {
			  ...state,
			  wiki: language
		  };
	  }
	  default:
		return state
	}
};

export default app;