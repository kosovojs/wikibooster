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
		this.setData = this.setData.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.saveArticle = this.saveArticle.bind(this);
		this.setAsIncorrect = this.setAsIncorrect.bind(this);
		this.toggleArticleEditing = this.toggleArticleEditing.bind(this);
	}

	saveArticle = (result) => (event) => {
		const {articleID, changedText, status} = this.state;
		const {task, article} = this.props;

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
				toast.info('Dati saglabāti', {autoClose:2000});
				this.props.goToNextArticle();
			} else {
				toast.warn('Notika kļūda', {autoClose:3500});
			}
		})
		.catch(data => {
			toast.warn('Notika kļūda', {autoClose:3500});
		});
	}
	
	setData() {
		const {task, article} = this.props;
		console.log(article);
		
		this.setState({loading: true});

		//http://127.0.0.1:5000/job/double/Magnolijas
		fetch(urlendpoint+'task/lvwiki/'+task+'/'+article)
		.then(response => response.json())
		.then(data => {
			const {status, origText, changedText, articleID, enFormatted} = data;

			const finalStatus = origText == null || changedText == null ? 'noaction' : status;
			
			this.setState({article, origText,loading: false,status:finalStatus, changedText, articleID,enFormatted});
		});
	}

	checkLoggedIn() {
		fetch(urlendpoint+'info')
		.then(response => response.json())
		.then(data => {
			const {status} = data;
			
			if (status === 'ok') {
				this.setState({isAuth: true});
			}
		});
	}

	setAsIncorrect() {
		this.props.goToNextArticle();
	}
	
	componentDidMount() {
		this.setData();
		this.checkLoggedIn();
	}

	componentDidUpdate(prevProps) {
		if (this.props.article !== prevProps.article || this.props.task !== prevProps.task) {
			this.setData();
		}
	}

	toggleArticleEditing() {
		this.setState({articleEditing: !this.state.articleEditing});
	}

	handleChange(event) {
		this.setState({changedText: event.target.value});
	}

  	render() {
		const {article, loading, error, origText,changedText, status, savingProcess,articleEditing, isAuth, enFormatted} = this.state;
		const {task} = this.props;

		const textareaText = task == '4' ? origText : changedText;

		return <div>
			{error ? <div>Notika kļūda</div> : <div>{loading ? <div>Ielādējam datus</div> : <div><h3>{article && article !== '' ? ArticleTitle(article,'lv') : ""}</h3>
				<div className="btn-group actionButtons" role="group">
  					<button disabled={savingProcess || !isAuth} type="button" className="btn btn-outline-success" onClick={this.saveArticle('success')}>Saglabāt</button>
  					<button disabled={savingProcess || !isAuth} type="button" className="btn btn-outline-info" onClick={this.props.goToNextArticle}>Izlaist</button>
 					<button disabled={savingProcess || !isAuth} type="button" className="btn btn-outline-danger" onClick={this.saveArticle('error')}>Rastā nav nepieciešama darbība</button>
 					<button disabled={savingProcess || !isAuth} type="button" className="btn btn-outline-info" onClick={this.toggleArticleEditing}>Veikt labojumus rakstā</button>
				</div>
			{status === 'noaction' ? <div className="noActionNeeded">Izskatās, ka šim rakstam nav nepieciešamas nekādas darbības, kas saistītas ar šo uzdevumu (spied "Saglabāt")</div> : <div>{task == '4' ? <div><InfoboxView lv={changedText} en={enFormatted} /></div> : <div><h4>Labojumi</h4>
				{origText === changedText ? <div className="noActionNeeded">Netika veiktas izmaiņas</div> : Comparision(origText,changedText)}</div>}
				{articleEditing || task == '4' ? <div>
				<h4>Labot tekstu</h4>
				Tev ir iespēja labot tekstu pirms tā saglabāšanas Vikipēdijā:
				<textarea className="form-control" rows={10}  value={textareaText} onChange={this.handleChange}/>
				</div> : ""}</div>
				
				}</div>}</div>}
		</div>;
	}
}