import { SET_WIKI_LANGUAGE, SET_WIKI_OPTIONS, NULLIFY_APP_STATE } from '../actions/app'

const defaultState = {
	wiki: null,
	wikis: []
};

const app = (state = defaultState, action) => {
	switch (action.type) {
		case SET_WIKI_LANGUAGE: {
			const { language } = action;

			return {
				...state,
				wiki: language
			};
		}
		case SET_WIKI_OPTIONS: {
			const { data } = action;

			return {
				...state,
				wikis: data
			};
		}
		case NULLIFY_APP_STATE: {
			return {
				...state,
				wiki: null
			};
		}
		default:
			return state
	}
};

export default app;