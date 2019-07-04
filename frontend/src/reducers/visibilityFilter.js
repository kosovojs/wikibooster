import { SET_VISIBILITY_FILTER } from '../actions/visibilityFilters'

const defaultState = {
	targetLanguage: '',
	originalLanguage: ''
};

const visibilityFilter = (state = defaultState, action) => {
  switch (action.type) {
    case SET_VISIBILITY_FILTER: {
		const {key, filter} = action;
		
		return {
			...state,
			[key]: filter
		};
	}
    default:
      return state
  }
}

export default visibilityFilter;