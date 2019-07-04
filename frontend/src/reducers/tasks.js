import {GET_TASKS, SET_TASK, SET_ARTICLE_LIST, REMOVE_FROM_LIST, SET_ARTICLE_LIST_LOADING, SET_ARTICLE, SET_ARTICLE_DATA, SET_ARTICLE_LOADING} from '../actions/tasks';

const defaultState = {
	taskId: null,
	description: [],
	articlesLoading: false,
	articleLoading: false,
	articles: [],
	currentArticle: {
		name: '',
		id: null,
		params: {
			origText: '',
			status: null,
			changedText: ''
		}
	}
};

const tasks = (state = defaultState, action) => {
	switch (action.type) {
	  case GET_TASKS: {
		  const {payload} = action;
		  
		  return {
			  ...state,
			  description: payload
		  };
	  }
	  case SET_TASK: {
		  const {id} = action;
		  
		  return {
			  ...state,
			  taskId: id,
			  articles: []
		  };
	  }
	  case SET_ARTICLE_LIST: {
		  const {list} = action;
		  
		  return {
			  ...state,
			  articles: list,
			  currentArticle: {
				  name: list[0],
				  id: 0,
				  params: {
					  origText: '',
					  status: null,
					  changedText: ''
				  
			  }
			  }
		  };
	  }
	  case SET_ARTICLE: {
		  const {article, key} = action;

		  const currentID = state.currentArticle.id;

		  let id = key;

		  if (typeof id === 'undefined') {

			id = (state.articles.length - currentID === 1) ? 0 : currentID+1;
		  }
		  
		  const title = typeof article === 'undefined' ? state.articles[id] : article;
		  
		  return {
			  ...state,
			  currentArticle: {
					...state.currentArticle,
				  name: title,
				  id: id
			  }
		  };
	  }
	  case SET_ARTICLE_DATA: {
		const {payload: {
			origText,status, changedText
		}} = action;
		
		  return {
			  ...state,
			  currentArticle: {
					...state.currentArticle,
					params: {
						origText,
						status,
						changedText
					}
			  }
		  };
	  }
	  case REMOVE_FROM_LIST: {
		  const {article: articleToRemove} = action;
		  
		  return {
			  ...state,
			  articles: state.articles.filter(article => article !== articleToRemove)
		  };
	  }
	  case SET_ARTICLE_LIST_LOADING: {
		  const {payload: newStatus} = action;
		  
		  return {
			  ...state,
			  articlesLoading: newStatus
		  };
	  }
	  case SET_ARTICLE_LOADING: {
		  const {payload: newStatus} = action;
		  
		  return {
			  ...state,
			  articleLoading: newStatus
		  };
	  }
	  default:
		return state;
	}
};

export default tasks;