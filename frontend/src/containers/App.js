import { connect } from 'react-redux';
import App from '../components/App';
import { setWikiLanguage } from '../actions/app';
import {checkAuth} from '../actions/auth';
import {getTasks} from '../actions/tasks';

import { urlendpoint } from '../config';

const DEFAULT_LANG = 'lv';

const mapDispatchToProps = (dispatch) => ({
	initialLoad: () => {
		dispatch(setWikiLanguage(DEFAULT_LANG));
		
		dispatch(setInitialAppData());
		
		dispatch(checkAuth());
	},
});

const setInitialAppData = () => {
	return function(dispatch, getState) {
		const state = getState();

		const currLanguage = state.app.wiki;

	  return fetch(`${urlendpoint}tasks/${currLanguage}wiki`)
		.then(
		  response => response.json(),
		  error => console.log('An error occurred.', error)
		)
		.then(json =>
		  dispatch(getTasks(json))
		)
	}
}

export default connect(
  null,
  mapDispatchToProps
)(App);