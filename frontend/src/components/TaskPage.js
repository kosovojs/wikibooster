import React, { Component } from 'react';
import Task from '../containers/Task';
import ArticleList from "../containers/ArticleList";
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
	
	setup() {
		const {id} = this.props.match.params;
		this.props.setTask(id);
	}

	componentDidMount() {
		this.setup();
	}

	componentDidUpdate(prevProps) {
		if (this.props.match.params.id !== prevProps.match.params.id) {
			this.setup();
		}
	}
  
  	render() {
	  const {articleId, loading, articles, taskId} = this.props;
	  const error = false;
	  
    return (<div>{error ? <div>Notika kļūda</div> : <div>{loading ? "Ielādējam datus" : <div>{articles.length> 0 ? <div>
		<div id="taskPageFormat">
			<div>
			<ArticleList />
			</div>
			<div id="taskArea">
		<Task />
			</div>
		</div>
	</div> : "Nav neviena raksta!"}</div>}</div>}
		</div>

    );
  }
}
// article={articles[articleId]} task={taskId} goToNextArticle={this.goToNextArticle}