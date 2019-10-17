import React, { Component } from 'react';
import { toast } from 'react-toastify';
import ReactTable from "react-table";
import TypoRow from "./TypoRow";
import "react-table/react-table.css";
import { urlendpoint } from '../config';

let setAll = (obj, val) => Object.keys(obj).forEach(k => obj[k] = val);

const cleanValue = (typoObject) => {
	let typoObject2 = Object.keys(typoObject).reduce(
		(accumulator, current) => {
		  accumulator[current] = null; 
		  return accumulator
		}, {});
	console.log(typoObject2);
	typoObject2.id = 0;
	return typoObject2;
}

export default class TypoManagement extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			error: false,
			data: [],
			page:0,
			expanded: {}
		};
	}

	setupDate = () => {
		const wiki = this.props.match.params.lang;

		/* this.setState({
			data: [{ "active": 1, "case": null, "comment": null, "dumpsearch": null, "minor": null, "name": "pa retam", "regex": 1, "replace_with": "\\1a retam", "search_for": "([Pp])aretam", "test_cases": null, "whole": null, id:1 }]
		}) */

		fetch(`${urlendpoint}typo/${wiki}`)
			.then(
				response => response.json(),
				error => console.log('An error occurred.', error)
			)
			.then(json =>
				
				this.setState({
					data: json
				})
			)


	}

	setAsIncorrect() {
		this.props.goToNextArticle();
	}

	componentDidMount() {
		this.setupDate();
	}

	componentDidUpdate(prevProps) {
		if (this.props.match.params.lang !== prevProps.match.params.lang) {
			this.setupDate();
		}
	}

	addNew = () => {
		const {page, data, expanded } = this.state;
		const numberOfRows = data.length;

		const lastPage = Math.round(numberOfRows/10);
		
		this.setState({
			data: [
				...this.state.data,
				cleanValue(this.state.data[0])
			],
			expanded: {
				...this.state.expanded,
				[numberOfRows]:{}
			},
			//page:lastPage
		})
	}

	handleDataUpdate = (typoData) => {
		/* const {active, rowID, name, replace_with, search_for, id, isNew} = typoData;
		const {data} = this.state;
		 */
	}

	render() {
		const { error, loading, data } = this.state;

		if (error) {
			return <div>Error!</div>
		}

		if (loading) {
			return <div>Loading...</div>
		}

		return <div>{data && data.length > 0 && <>
			<ReactTable
				data={data}
				columns={[
					{
						Header: "Name",
						accessor: "name"
					},
					{
						Header: "What to search for?",
						accessor: "search_for"
					},
					{
						Header: "What to replace with",
						accessor: "replace_with"
					}
				]}
				defaultPageSize={10}
				className="-striped -highlight"
				SubComponent={(row) => {
					return <TypoRow data={row.row._original} onDataUpdate={this.handleDataUpdate} row={row.index} />
				}}
				page={this.state.page}
				expanded={this.state.expanded}
				onPageChange={page => this.setState({ page })}
				onExpandedChange={expanded => this.setState({ expanded })}
			/>
		</>}
		<button onClick={this.addNew} type="button" className="btn btn-primary">Add new typo!</button>
		</div>;
	}
}