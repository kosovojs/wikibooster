import React, { Component } from 'react';
import { toast } from 'react-toastify';
import { urlendpoint } from '../config';

import { withRouter } from "react-router";

class TypoRow extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			error: false,
			data: {},
			/* tests: [
				{test: '', expected: '', result: true, actual: ''}
			] */
		};
	}

	setupDate = () => {
		this.setState({
			data: this.props.data
		})
	}

	componentDidMount() {
		this.setupDate();
	}

	handleChange = (key, section = 'data') => (event) => {
		let value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;

		this.setState({
			[section]: {
				...this.state[section],
				[key]: value
			}
		});
	}

	handleTestChange = (key, section = 'data') => (event) => {
		let value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;

		let tests = [...this.state.tests];
		let item = { ...tests[key] };
		item[section] = value;
		tests[key] = item;

		this.setState({ tests }, () => console.log(this.state, key, section));
	}

	componentDidUpdate(prevProps) {/* 
		if (this.props.match.params.lang !== prevProps.match.params.lang) {
			this.setupDate();
		} */
	}

	addNewTest = () => {
		this.setState(state => {
			const list = [...state.tests, { test: '', expected: '', result: true, actual: '' }];
			return {
				tests: list
			};
		});
	}

	saveData = () => {
		const { search_for, id } = this.state.data;
		if (search_for.trim() === '') {
			toast.warn("Add at least search phrase", { autoClose: 5000 });
			return;
		}

		console.log(this.props.match.params)
		const dataToSend = Object.assign({}, this.state.data, { wiki: this.props.match.params.lang });

		fetch(`${urlendpoint}save_typo`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dataToSend) })
			.then(
				response => response.json(),
				error => console.log('An error occurred.', error)
			)
			.then(json => {
				if (json.status === 'ok') {
					toast.success("Typo saved!", { autoClose: 4000 });
					const dataToSendToParent = Object.assign({}, this.state.data, { id: json.id, isNew: id == 0, rowID: this.props.row });

					this.props.onDataUpdate(dataToSendToParent);
				}
			}
			)
	}

	render() {
		const { data } = this.state;

		return <div style={{ width: '99%' }}>
			<div className="form-row">
				<div className="form-group col-md-4">
					<label for="inputTitle">Title</label>
					<input type="text" className="form-control" id="inputTitle" value={data.name} onChange={this.handleChange('name')} />
				</div>
				<div className="form-group col-md-4">
					<label for="inputFrom">What to search for?</label>
					<input type="text" className="form-control" id="inputFrom" value={data.search_for} onChange={this.handleChange('search_for')} />
				</div>
				<div className="form-group col-md-4">
					<label for="inputTo">What to replace with?</label>
					<input type="text" className="form-control" id="inputTo" value={data.replace_with} onChange={this.handleChange('replace_with')} />
				</div>
			</div>
			<div className="form-row">
				<div className="form-group col-md-4">
					<label for="inputComment">Comment</label>
					<textarea className="form-control" id="inputComment" value={data.comment} onChange={this.handleChange('comment')}></textarea>
				</div>
				{/* regex: false, case: false, wholeWorld:true, active: true, dump: false, minor: true */}
				<div className="form-group col-md-4">
					<div className="form-check">
						<input className="form-check-input" type="checkbox" id="activeCheck" checked={data.active} onChange={this.handleChange('active')} />
						<label className="form-check-label" for="activeCheck">Active</label>
					</div>
					<div className="form-check">
						<input className="form-check-input" type="checkbox" id="regexCheck" checked={data.regex} onChange={this.handleChange('regex')} />
						<label className="form-check-label" for="regexCheck">Is regex</label>
					</div>
					<div className="form-check">
						<input className="form-check-input" type="checkbox" id="caseCheck" checked={data.case} onChange={this.handleChange('case')} />
						<label className="form-check-label" for="caseCheck">Case sensitive</label>
					</div>
				</div>
				<div className="form-group col-md-4">
					<div className="form-check">
						<input className="form-check-input" type="checkbox" id="wholeWorldCheck" checked={data.whole} onChange={this.handleChange('whole')} />
						<label className="form-check-label" for="wholeWorldCheck">Match whole words</label>
					</div>
					<div className="form-check">
						<input className="form-check-input" type="checkbox" id="dumpCheck" checked={data.dumpsearch} onChange={this.handleChange('dumpsearch')} />
						<label className="form-check-label" for="dumpCheck">Search dump</label>
					</div>
					<div className="form-check">
						<input className="form-check-input" type="checkbox" id="minorCheck" checked={data.minor} onChange={this.handleChange('minor')} />
						<label className="form-check-label" for="minorCheck">Is minor</label>
					</div>
				</div>
			</div>
			{/* <h4>Test-cases <span style={{fontSize:'small'}}>(<span style={{cursor:'pointer'}} onClick={this.addNewTest} title="add new test-case">+</span>)</span></h4>
			{tests.map((test, key) => <div className="form-row">
				<div className="form-group col-md-4">
					<label for={`inputTest${key}Text`}>Test text</label>
					<textarea className="form-control" id={`inputTest${key}Text`} value={test.test} onChange={this.handleTestChange(key,'test')}></textarea>
				</div>
				<div className="form-group col-md-4">
					<label for={`inputTest${key}Expected`}>Expected text</label>
					<textarea className="form-control" id={`inputTest${key}Expected`} value={test.expected} onChange={this.handleTestChange(key,'expected')}></textarea>
				</div>
				<div className="form-group col-md-4">
					<label for={`inputTest${key}Actual`}>Actual text</label>
					<textarea className="form-control" id={`inputTest${key}Actual`} value={test.actual}></textarea>
				</div>
			</div>)} */}

			<button type="button" className="btn btn-primary" onClick={this.saveData}>Save</button>
		</div>;
	}
}

export default withRouter(TypoRow);