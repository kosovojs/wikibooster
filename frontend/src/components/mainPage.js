import React from 'react';
import {connect} from 'react-redux';

import './mainPage.scss';

//https://daveceddia.com/access-redux-store-outside-react/

const MainPage = (props) => {
	const handleClick = (id) => (event) => {
		window.location = '#/task/'+id;
	}

	const {tasks} = props;

	//const state = store.getState();
	//const tasks = state.tasks.description;
	//console.log(tasks);
	
	return <div className="container">
		<h2><i>WikiBooster</i></h2>
		<h4><i>rīks, kas atvieglo tipveida problēmu novēršanu</i></h4>
		
		<div className="tasks">{tasks.map((task, key) => <div className="myCard" key={key}><span className="title" onClick={handleClick(task.url_id)}>{task.task}</span><br /><span className="description">{task.description}</span></div>)}</div></div>
};

const mapStateToProps = (state) => ({
	tasks: state.tasks.description
});

export default connect(
	mapStateToProps
)(MainPage);