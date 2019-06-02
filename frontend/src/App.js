import 'bootstrap/dist/css/bootstrap.css';
import React, { Component } from 'react';
import './App.css';
import { HashRouter as Router, Route, Switch  } from 'react-router-dom';
//import ArticleList from './components/articleList';
import TaskPage from './components/TaskPage';
import MainPage from './components/mainPage';
import Header from './Header';
import {urlendpoint} from './config';

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const NotFound = ({ location }) => (
	<div>
	  <h3>Did not found page for <code>{location.pathname}</code></h3>
	</div>
);

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			isAuth: false,
			userName: ''
		};
	}

	componentDidMount() {
		fetch(urlendpoint+'info')
		.then(response => response.json())
		.then(data => {
			const {status, username} = data;

			console.log(data);
			if (status === 'ok') {
				this.setState({isAuth: true, userName: username});
			}
		});
	}
  	render() {
		  const {isAuth, userName} = this.state;

    return (
		<Router>
		  <div>
		  	<Header isAuth={isAuth} userName={userName} />
			<Switch>
			  <Route exact path="/" component={MainPage} />
			  <Route exact path="/task/:id" component={TaskPage} />
			  <Route component={NotFound} />
			</Switch>
            <ToastContainer
            position="bottom-right"
            autoClose={2500}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnVisibilityChange
            draggable={false}
            pauseOnHover
            />
		  </div>
		</Router>

    );
  }
}

export default App;