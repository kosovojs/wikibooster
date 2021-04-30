import { connect } from 'react-redux';
import App from '../components/App';
import { setWikiLanguage, setWikiOptions } from '../actions/app';
import { checkAuth } from '../actions/auth';

import { urlendpoint } from '../config';

const DEFAULT_LANG = 'lv';

const mapDispatchToProps = (dispatch) => ({
	initialLoad: () => {
		dispatch(setWikiLanguages());
		//dispatch(setWikiLanguage(DEFAULT_LANG));

		//dispatch(setInitialAppData());

		dispatch(checkAuth());
	},
});

const setWikiLanguages = () => {
	return function (dispatch, getState) {

		return fetch(`${urlendpoint}wikis`)
			.then(
				response => response.json(),
				error => console.log('An error occurred.', error)
			)
			.then(json =>
				dispatch(setWikiOptions(json))
			)
	}
}

export default connect(
	null,
	mapDispatchToProps
)(App);
