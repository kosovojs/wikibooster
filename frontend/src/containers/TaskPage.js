import { connect } from 'react-redux';
import TaskPage from '../components/TaskPage';
import {setTask, setArticlesToList, setArticleListLoading} from '../actions/tasks';

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

const mapDispatchToProps = (dispatch) => ({
	setTask: (id) => {
		dispatch(setTask(id));
		dispatch(setArticleList());
	},
});

const setArticleList = () => {
	return function(dispatch, getState) {
		dispatch(setArticleListLoading(true));

		const state = getState();

		const currTask = state.tasks.taskId;
		const lang = state.app.wiki;

	  return fetch(`${urlendpoint}task/${lang}wiki/${currTask}/articles`)
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

export default connect(
	mapStateToProps,
  	mapDispatchToProps
)(TaskPage);