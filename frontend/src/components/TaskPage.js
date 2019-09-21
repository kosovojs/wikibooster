import React, { Component } from 'react';
import Task from '../containers/Task';
import ArticleList from "../containers/ArticleList";
import './taskPage.scss';

export default class TaskPage extends Component {
	setup() {
		const { id } = this.props.match.params;
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
		const { loading, articles } = this.props;
		const error = false;

		return (<div>{error ? <div>Error</div> : <div>{loading ? "Loading" : <div>{articles.length > 0 ? <div>
			<div id="taskPageFormat">
				<div>
					<ArticleList />
				</div>
				<div id="taskArea">
					<Task />
				</div>
			</div>
		</div> : "No articles!"}</div>}</div>}
		</div>

		);
	}
}
// article={articles[articleId]} task={taskId} goToNextArticle={this.goToNextArticle}