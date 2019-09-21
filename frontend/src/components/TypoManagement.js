import React, { Component } from 'react';
import { toast } from 'react-toastify';
import ReactTable from "react-table";
import TypoRow from "./TypoRow";
import "react-table/react-table.css";

export default class TypoManagement extends Component {
	constructor(props) {
		super(props);
		this.state = {
			loading: false,
			error: false,
			data: []
		};
		this.handleChange = this.handleChange.bind(this);
		this.saveArticle = this.saveArticle.bind(this);
		this.setAsIncorrect = this.setAsIncorrect.bind(this);
		this.toggleArticleEditing = this.toggleArticleEditing.bind(this);
		this.toggleArticleEditing1 = this.toggleArticleEditing1.bind(this);
		this.setTextareaText = this.setTextareaText.bind(this);
	}

	setupDate = () => {
		this.setState({
			data: [
				{ title: 'dfsdf', from: 'dfsdfsf', to: 'fsdfdfsdfsd' }
			]
		})
	}

	saveArticle = (result) => (event) => {
		const { isAuth } = this.props;

		if (!isAuth) {
			toast.warn("You have to log-in to save actions", { autoClose: 5000 });
			return;
		}

		this.props.saveArticleData({ result, textForSave: this.state.textAreaText });
	}

	setAsIncorrect() {
		this.props.goToNextArticle();
	}

	setTextareaText() {
		if (typeof this.props.articleParams.changedText !== 'undefined') {
			const textToAdd = this.props.articleParams.changedText;

			this.setState({ textAreaText: textToAdd });
		}
	}

	componentDidMount() {
		this.setupDate();
	}

	componentDidUpdate(prevProps) {
		if (this.props.match.params.lang !== prevProps.match.params.lang) {
			this.setupDate();
		}
	}

	toggleArticleEditing(newValue = !this.state.articleEditing) {
		this.setState({ articleEditing: newValue });
	}

	toggleArticleEditing1() {
		this.setState({ articleEditing: !this.state.articleEditing });
	}

	handleChange(event) {
		this.setState({ textAreaText: event.target.value });
	}

	render() {
		const { error, loading, data } = this.state;

		if (error) {
			return <div>Error!</div>
		}

		if (loading) {
			return <div>Loading...</div>
		}

		return <div>{/*data && data.length > 0 && <>
			{JSON.stringify(data)}

			<ReactTable
				data={data}
				columns={[
					{
						Header: "Name",
						accessor: "title"
					},
					{
						Header: "What to search for?",
						accessor: "from"
					},
					{
						Header: "What to replace with",
						accessor: "to"
					}
				]}
				defaultPageSize={10}
				className="-striped -highlight"
				SubComponent={(row) => {
					console.log(row.row._original);
					return <TypoRow data={row.row._original} />
				}}
			/>
			</>*/
			
			<TypoRow data={{ title: 'dfsdf', from: 'dfsdfsf', to: 'fsdfdfsdfsd', comment:'fsdfsdfsdfsdfsdf', regex: false, case: false, wholeWorld:true, active: true, dump: false, minor: true }} />
			
			}
		</div>;
	}
}