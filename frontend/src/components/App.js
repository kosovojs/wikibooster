import 'bootstrap/dist/css/bootstrap.css';
import React, { useEffect } from 'react';
import { HashRouter as Router, Route, Switch  } from 'react-router-dom';
//import ArticleList from './components/articleList';
import TaskPage from '../containers/TaskPage';
import MainPage from './mainPage';
import TypoManagement from './TypoManagement';
import Header from '../containers/Header';
//import {Footer} from '../Footer';

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import TypoPage from '../containers/TypoPage';

const NotFound = ({ location }) => (
	<div>
	  <h3>Did not found page <code>{location.pathname}</code></h3>
	</div>
);

function App(props) {
	//https://stackoverflow.com/questions/38563679/react-redux-dispatch-action-on-app-load-init
   useEffect(() => props.initialLoad(), []);

  return (
	<Router>
		  <Header />
		<Switch>
		  <Route exact path="/typofix" component={TypoPage} />
		  <Route exact path="/:lang?" component={MainPage} />
		  <Route exact path="/:lang/task/:id" component={TaskPage} />
		  <Route exact path="/:lang/typo" component={TypoManagement} />
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
		{/* <Footer /> */}
	</Router>
  );
}

export default App;
