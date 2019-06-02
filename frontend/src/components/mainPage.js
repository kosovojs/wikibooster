import React from 'react';
import './mainPage.scss';
import {tasks} from '../config';

const MainPage = () => {
	const handleClick = (id) => (event) => {
		window.location = '#/task/'+id;
	}
	

	return <div className="tasks">{tasks.map((task, key) => <div className="myCard" key={key}><span className="title" onClick={handleClick(task.id)}>{task.title}</span><br /><span className="description">{task.description}</span></div>)}</div>
};

export default MainPage;