import { connect } from 'react-redux';
import Task from '../components/task';
import { setArticleData, setArticleLoading, setArticle, setArticleSaving, hadleTextChange } from '../actions/tasks';


import { toast } from 'react-toastify';

import { urlendpoint } from '../config';

const mapStateToProps = (state) => ({
	lang: state.app.wiki,
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
	},
	saveArticleData: (data) => {
		dispatch(handleArticleSave(data));
	},
	setChangedText: (newText) => {
		dispatch(hadleTextChange(newText));
	}
});

const handleArticleSet = () => {
	return function (dispatch, getState) {
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

				const { status, origText, changedText } = json;

				const finalStatus = origText == null || changedText == null ? 'noaction' : status;

				dispatch(setArticleData({ origText, status: finalStatus, changedText }));

				dispatch(setArticleLoading(false));
			})
	}
}

const handleArticleSave = (props) => {
	return function (dispatch, getState) {
		dispatch(setArticleSaving(true));

		const state = getState();

		const currTask = state.tasks.taskId;
		const lang = state.app.wiki;
		
		const { name:articleTitle, params: { changedText, status } } = state.tasks.currentArticle;

		const {result} = props;//ok/error
		
		const dataToSend = {
			wiki: lang,
			job: currTask,
			status,//check for 'noaction'
			article: articleTitle,//articleID == null ? 0 : articleID,
			result,
			wikitext: changedText == null ? '' : changedText
		};
		
		return fetch(urlendpoint + 'save', { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dataToSend) })
			.then(
				response => response.json(),
				error => console.log('An error occurred.', error)
			)
			.then(data => {
				dispatch(setArticleSaving(false));
				
				if (data.status === 'ok' || data.status === 'info') {
					toast.info('Dati saglabāti', { autoClose: 3000 });
					dispatch(setArticle({}));
				} else {
					toast.warn('Notika kļūda', { autoClose: 4500 });
				}
			})
			.catch(data => {
				dispatch(setArticleSaving(false));
				toast.warn('Notika kļūda', { autoClose: 4500 });
			});
	}
}

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Task);