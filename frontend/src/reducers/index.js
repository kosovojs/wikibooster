import { combineReducers } from 'redux';
import app from './app';
//import articles from './articles';
import auth from './auth';
import tasks from './tasks';

export default combineReducers({
	app,
	//articles,
	auth,
	tasks
})