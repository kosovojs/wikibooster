import React, { Component } from 'react';
import Task from './task';
import ArticleList from "./articleList";
import {urlendpoint} from '../config';
import './taskPage.scss';

export default class TaskPage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			articleId: 0,
			articles: [],
			loading: false,
			error: false
		};

		this.goToNextArticle = this.goToNextArticle.bind(this);
		this.saveArticleAction = this.saveArticleAction.bind(this);
		this.handleArticleChange = this.handleArticleChange.bind(this);
	}
	
	handleArticleChange = (article,articleId) => (event) => {
		console.log(article,articleId);

		this.setState({articleId});
	}

	goToNextArticle() {
		const {articles, articleId} = this.state;
		
		
		const newId = (articles.length - articleId === 1) ? 0 : articleId+1;
		this.setState({articleId:newId});
	}

	saveArticleAction() {
		
	}

	setup() {
		const {id:task} = this.props.match.params;

		const debug = false;
		
		this.setState({loading: true});
		
		if (debug) {
			const articles = ['a','b','b','b','b','b'];
			const articleId = 0;
	
			this.setState({
				articles,
				articleId,
				loading: false,
				error: false
			});

		} else {
			//task/<wiki>/<task_id>/articles
			fetch(urlendpoint+'task/lvwiki/'+task+'/articles')
			.then(response => response.json())
			.then(data => {
				this.setState({articles:data,loading: false,articleId:0});
			});
		}
	}

	componentDidMount() {
		this.setup();
		//this.props.onArticleChange();
	}

	componentDidUpdate(prevProps) {
		if (this.props.match.params.id !== prevProps.match.params.id) {
			this.setup();
		}
	}
  
  	render() {
	  const {articleId, error, loading, articles} = this.state;
	  const {id:taskId} = this.props.match.params;
	  
    return (<div>{error ? <div>Notika kļūda</div> : <div>{loading ? "Ielādējam datus" : <div>
		<div id="taskPageFormat">
			<div>
			<ArticleList handleArticleSelect={this.handleArticleChange} articles={articles} articleId={articleId} />
			</div>
			<div id="taskArea">
		<Task article={articles[articleId]} task={taskId} goToNextArticle={this.goToNextArticle} />
			</div>
		</div>
</div>}</div>}
		</div>

    );
  }
}