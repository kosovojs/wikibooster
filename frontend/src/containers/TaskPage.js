import { connect } from 'react-redux';
import TaskPage from '../components/TaskPage';
import {setTask, setArticlesToList, setArticleListLoading} from '../actions/tasks';
import { setWikiLanguage } from '../actions/app';

import { withRouter } from "react-router";

import { urlendpoint } from '../config';
/*

const defaultState = {
	taskId: null,
	description: [],
	articlesLoading: false,
	articles: []
};

*/

const mapStateToProps = (state) => ({
	articles: state.tasks.articles,
	loading: state.tasks.articlesLoading,
	articleId: state.tasks.currentArticle.id,
	taskId: state.tasks.taskId//pēc tam izņemt
});

const mapDispatchToProps = (dispatch, ownProps) => ({
	setTask: (id) => {
		dispatch(setTask(id));

		dispatch(setArticleList(ownProps.match.params.lang));
	},
});

const setArticleList = (langProp) => {
	return function(dispatch, getState) {
		dispatch(setArticleListLoading(true));

		const state = getState();

		if (state.app.wiki === null) {
			dispatch(setWikiLanguage(langProp));
		}

		const currTask = state.tasks.taskId;
		const lang = state.app.wiki;

	  return fetch(`${urlendpoint}task/${lang}/${currTask}/articles`)
		.then(
		  response => response.json(),
		  error => console.log('An error occurred.', error)
		)
		.then(json => {
			dispatch(setArticlesToList(json));
			dispatch(setArticleListLoading(false));
		})
	}
}

export default withRouter(connect(
	mapStateToProps,
  	mapDispatchToProps
)(TaskPage));