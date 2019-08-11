import React, { Component } from 'react';
//import WikEdDiff from '../WikEdDiff';
//let WikEdDiff = require('../WikEdDiff'); 
import Comparision from '../components/comparision';
import ArticleTitle from './articleTitle';
import InfoboxView from './infoboxView';
import { toast } from 'react-toastify';

export default class Task extends Component {
	constructor(props) {
		super(props);
		this.state = {
			origText: "",
			loading: true,
			error: false,
			isAuth: false,
			status: '',
			articleEditing: false,
			savingProcess: false//saglabāšanas process, lai diseiblotu pogas
		};
		this.handleChange = this.handleChange.bind(this);
		this.saveArticle = this.saveArticle.bind(this);
		this.setAsIncorrect = this.setAsIncorrect.bind(this);
		this.toggleArticleEditing = this.toggleArticleEditing.bind(this);
		this.toggleArticleEditing1 = this.toggleArticleEditing1.bind(this);
	}

	saveArticle = (result) => (event) => {
		const { isAuth } = this.props;

		if (!isAuth) {
			toast.warn("You have to log-in to save actions", { autoClose: 5000 });
			return;
		}

		this.props.saveArticleData({result});
	}

	setAsIncorrect() {
		this.props.goToNextArticle();
	}

	componentDidMount() {
		this.props.setArticleData();
	}

	componentDidUpdate(prevProps) {
		if (this.props.article !== prevProps.article || this.props.task !== prevProps.task) {
			this.props.setArticleData();
			this.toggleArticleEditing(false);
		}
	}

	toggleArticleEditing(newValue = !this.state.articleEditing) {
		this.setState({ articleEditing: newValue });
	}

	toggleArticleEditing1() {
		this.setState({ articleEditing: !this.state.articleEditing });
	}

	handleChange(event) {
		this.props.setChangedText(event.target.value);
	}

	render() {
		const { article, loading, articleParams: { origText, changedText, status }, isAuth, task, lang } = this.props;
		const { articleEditing } = this.state;
		const error = false;

		const savingProcess = false;
		const textareaText = changedText;//task == '4' ? origText : changedText;

		return <div>
			{error ? <div>Error!</div> : <div>{loading ? <div>Loading</div> : <div><h3>{article && article !== '' ? ArticleTitle(article, lang) : ""}</h3>
				{!isAuth && <div className="alert alert-primary" role="alert">
					You have to <a href="//tools.wmflabs.org/booster/login" className="alert-link">log-in</a> to save actions!
				</div>}
				<div className="btn-group actionButtons" role="group">
					<button disabled={savingProcess} type="button" className="btn btn-outline-success" onClick={this.saveArticle('success')}>Save</button>
					<button disabled={savingProcess} type="button" className="btn btn-outline-info" onClick={this.props.goToNextArticle}>Skip</button>
					<button disabled={savingProcess} type="button" className="btn btn-outline-danger" onClick={this.saveArticle('error')}>No action needed</button>
					{/*<button disabled={savingProcess} type="button" className="btn btn-outline-info" onClick={this.toggleArticleEditing1}>Veikt labojumus rakstā</button>*/}
				</div>
				{status === 'noaction' ? <div className="noActionNeeded">No action needed for this article (press "Save")</div> : <div><h4>Edits</h4>
					{origText === changedText ? <div className="noActionNeeded">Netika veiktas izmaiņas</div> : Comparision(origText, changedText)}</div>}
				{articleEditing ? <div>
					<h4>Labot tekstu</h4>
					Tev ir iespēja labot tekstu pirms tā saglabāšanas Vikipēdijā:
				<textarea className="form-control" rows={10} value={changedText} onChange={this.handleChange} />
				</div> : ""}</div>

			}</div>}
		</div>;
	}
}