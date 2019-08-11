export const GET_TASKS = 'GET_TASKS';
export const SET_TASK = 'SET_TASK';
export const SET_ARTICLE_LIST = 'SET_ARTICLE_LIST';
export const REMOVE_FROM_LIST = 'REMOVE_FROM_LIST';
export const SET_ARTICLE_LIST_LOADING = 'SET_ARTICLE_LIST_LOADING';
export const SET_ARTICLE = 'SET_ARTICLE';
export const SET_ARTICLE_DATA = 'SET_ARTICLE_DATA';
export const SET_ARTICLE_LOADING = 'SET_ARTICLE_LOADING';
export const SET_ARTICLE_SAVING = 'SET_ARTICLE_SAVING';
export const HANDLE_TEXT_CHANGE = 'HANDLE_TEXT_CHANGE';

export const setArticle = ({article, key}) => ({//article - title, key - ID
	type: SET_ARTICLE,
	article,
	key
});

export const hadleTextChange = (newText) => ({
	type: HANDLE_TEXT_CHANGE,
	newText
})

export const setArticleData = ({origText,status, changedText}) => ({
	type: SET_ARTICLE_DATA,
	payload: {
		origText,status, changedText
	}
});

export const setArticleLoading = (status) => ({
	type: SET_ARTICLE_LOADING,
	payload: status
});

export const setArticleSaving = (status) => ({
	type: SET_ARTICLE_SAVING,
	payload: status
});

export const setArticleListLoading = (status) => ({
	type: SET_ARTICLE_LIST_LOADING,
	payload: status
});

export const getTasks = (taskData) => ({
	type: GET_TASKS,
	payload: taskData
});

export const setTask = (id) => ({
	type: SET_TASK,
	id
});

export const setArticlesToList = (list) => ({
	type: SET_ARTICLE_LIST,
	list
});

export const removeArticleFromList = (article) => ({
	type: REMOVE_FROM_LIST,
	article
});