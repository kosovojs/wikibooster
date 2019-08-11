import React, {useEffect} from 'react';
import { connect } from 'react-redux';
import { setWikiLanguage, nullifyAppState } from '../actions/app';
import { getTasks } from '../actions/tasks';

import { withRouter } from "react-router";

import { urlendpoint } from '../config';

import './mainPage.scss';

//https://daveceddia.com/access-redux-store-outside-react/

const MainPage = (props) => {
	const handleClick = (id, hasArticles) => (event) => {
		if (hasArticles === null) {
			return;
		}
		window.location = `#/${wiki}/task/${id}`;
	}

	const handleClickWiki = (wiki) => (event) => {
		window.location = '#/' + wiki;
		props.setWikiLang(wiki);
	}

	useEffect(() => {
		const wikiLang = props.match.params.lang;
		if (wikiLang) {
			props.setWikiLang(wikiLang);
		} else {
			props.setInitialState();
		}
	}, [props.match.params.lang]);

	const { tasks, wiki, wikis } = props;

	return <div className="container">
		<h2><i>WikiBooster</i></h2>
		{wikis.length>0 && wiki === null && 
		<>
		Choose Wikipedia to work on!
		<div className="wikis">
			{wikis.map((wikiLang, key) => <div className="myCard" key={key} style={{cursor: 'pointer'}} onClick={handleClickWiki(wikiLang)}>{wikiLang}</div>)}
		</div>
		</>
		}

		{wiki && <>{tasks.length > 0 ? 
		<div className="tasks">
			{tasks.map((task, key) => <div className="myCard" key={key}><span className={"title" + (task.hasArticles ? ' clickable' : '')} onClick={handleClick(task.url_id, task.hasArticles)}>{task.task}</span><br /><span className="description">{task.description}</span>{task.hasArticles == null && <span className="noArticles">no articles</span>}</div>)}
		</div> : "No tasks currently available for this Wikipedia"}</>
		}
	</div>
};

const mapStateToProps = (state) => ({
	tasks: state.tasks.description,
	wikis: state.app.wikis,
	wiki: state.app.wiki
});

const mapDispatchToProps = (dispatch) => ({
	setWikiLang: (lang) => {
		dispatch(setWikiLanguage(lang));

		dispatch(setInitialAppData());
	},
	setInitialState: () => {
		dispatch(nullifyAppState());
	}
});

const setInitialAppData = () => {
	return function (dispatch, getState) {
		const state = getState();

		const currLanguage = state.app.wiki;

		return fetch(`${urlendpoint}tasks/${currLanguage}`)
			.then(
				response => response.json(),
				error => console.log('An error occurred.', error)
			)
			.then(json =>
				dispatch(getTasks(json))
			)
	}
}

export default withRouter(connect(
	mapStateToProps,
	mapDispatchToProps
)(MainPage));