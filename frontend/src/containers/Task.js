import { connect } from 'react-redux';
import Task from '../components/task';
import {setArticleData, setArticleLoading, setArticle} from '../actions/tasks';

import { urlendpoint } from '../config';

const mapStateToProps = (state) => ({
	isAuth: state.auth.isAuth,
	article: state.tasks.currentArticle.name,
	loading: state.tasks.articleLoading,
	articleParams: state.tasks.currentArticle.params,
	task: state.tasks.taskId//pēc tam izņemt
});

const mapDispatchToProps = (dispatch) => ({
	setArticleData: () => {
		dispatch(handleArticleSet());
	},
	goToNextArticle: () => {
		dispatch(setArticle({}));
	}
});

const handleArticleSet = () => {
	return function(dispatch, getState) {
		dispatch(setArticleLoading(true));

		const state = getState();

		const currTask = state.tasks.taskId;
		const articleTitle = state.tasks.currentArticle.name;
		const lang = state.app.wiki;
		
	  return fetch(`${urlendpoint}task/${lang}wiki/${currTask}/${articleTitle}`)
		.then(
		  response => response.json(),
		  error => console.log('An error occurred.', error)
		)
		.then(json => {
			
			const {status, origText, changedText} = json;

			const finalStatus = origText == null || changedText == null ? 'noaction' : status;
			
			dispatch(setArticleData({origText,status:finalStatus, changedText}));
			
			dispatch(setArticleLoading(false));
		})
	}
}

export default connect(
	mapStateToProps,
  	mapDispatchToProps
)(Task);