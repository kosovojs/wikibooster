import 'bootstrap/dist/css/bootstrap.css';
import React, { useEffect } from 'react';
import '../css/App.css';
import { HashRouter as Router, Route, Switch  } from 'react-router-dom';
//import ArticleList from './components/articleList';
import TaskPage from '../containers/TaskPage';
import MainPage from './mainPage';
import Header from '../containers/Header';
//import {Footer} from '../Footer';
import {urlendpoint} from '../config';

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const NotFound = ({ location }) => (
	<div>
	  <h3>Netika atrasta <code>{location.pathname}</code> lapa</h3>
	</div>
);

function App(props) {
	//https://stackoverflow.com/questions/38563679/react-redux-dispatch-action-on-app-load-init
  useEffect(() => props.initialLoad(), []);

  return (
	<Router>
		  <Header />
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
		{/*<Footer />*/}
	</Router>
  );
}

export default App;