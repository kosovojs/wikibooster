import React, { Component } from 'react';
//import WikEdDiff from '../WikEdDiff';
//let WikEdDiff = require('../WikEdDiff'); 
import Comparision from '../components/comparision';
import ArticleTitle from './articleTitle';
import {urlendpoint} from '../config';
import { toast } from 'react-toastify';
import InfoboxView from './infoboxView';

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
	}

	saveArticle = (result) => (event) => {
		const {articleID, changedText, status, isAuth} = this.state;
		const {task, article} = this.props;

		if (!isAuth) {
			toast.warn("Jāielogojas, lai saglabātu rakstus!",{autoClose:5000});
			return;
		}

		this.setState({savingProcess:true});
		const dataToSend = {
			job:task,
			status,//check for 'noaction'
			article:article,//articleID == null ? 0 : articleID,
			result,
			wikitext: changedText == null ? '' : changedText
		};
		
		fetch(urlendpoint+'save',{method: "POST",headers: {"Content-Type": "application/json"},body: JSON.stringify(dataToSend)})
		.then(response => response.json())
		.then(data => {
			this.setState({savingProcess:false});
			console.log('resp no save',data);
			if (data.status === 'ok' || data.status === 'info') {
				toast.info('Dati saglabāti', {autoClose:3000});
				this.props.goToNextArticle();
			} else {
				toast.warn('Notika kļūda', {autoClose:4500});
			}
		})
		.catch(data => {
			this.setState({savingProcess:false});
			toast.warn('Notika kļūda', {autoClose:4500});
		});
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
		}
	}

	toggleArticleEditing() {
		this.setState({articleEditing: !this.state.articleEditing});
	}

	handleChange(event) {
		this.setState({changedText: event.target.value});
	}

  	render() {
		const {article, loading, articleParams: {origText,changedText, status}, articleEditing, isAuth, task} = this.props;
		const error = false;

		const savingProcess = false;
		const textareaText = task == '4' ? origText : changedText;

		return <div>
			{error ? <div>Notika kļūda</div> : <div>{loading ? <div>Ielādējam datus</div> : <div><h3>{article && article !== '' ? ArticleTitle(article,'lv') : ""}</h3>
				{!isAuth && <div className="alert alert-primary" role="alert">
					Tev ir <a href="//tools.wmflabs.org/booster/login" className="alert-link">jāielogojas</a>, lai saglabātu savas darbības!
				</div>}
				<div className="btn-group actionButtons" role="group">
  					<button disabled={savingProcess} type="button" className="btn btn-outline-success" onClick={this.saveArticle('success')}>Saglabāt</button>
  					<button disabled={savingProcess} type="button" className="btn btn-outline-info" onClick={this.props.goToNextArticle}>Izlaist</button>
 					<button disabled={savingProcess} type="button" className="btn btn-outline-danger" onClick={this.saveArticle('error')}>Rakstā nav nepieciešama darbība</button>
 					<button disabled={savingProcess} type="button" className="btn btn-outline-info" onClick={this.toggleArticleEditing}>Veikt labojumus rakstā</button>
				</div>
			{status === 'noaction' ? <div className="noActionNeeded">Izskatās, ka šim rakstam nav nepieciešamas nekādas darbības, kas saistītas ar šo uzdevumu (spied "Saglabāt")</div> : <div><h4>Labojumi</h4>
				{origText === changedText ? <div className="noActionNeeded">Netika veiktas izmaiņas</div> : Comparision(origText,changedText)}</div>}
				{articleEditing ? <div>
				<h4>Labot tekstu</h4>
				Tev ir iespēja labot tekstu pirms tā saglabāšanas Vikipēdijā:
				<textarea className="form-control" rows={10}  value={textareaText} onChange={this.handleChange}/>
				</div> : ""}</div>
				
				}</div>}
		</div>;
	}
}