import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import AppContainer from './containers/App';

import { Provider } from 'react-redux';
import store from './store';

import '@fortawesome/fontawesome-free/css/fontawesome.min.css';
import '@fortawesome/fontawesome-free/css/solid.css';
import '@fortawesome/fontawesome-free/css/brands.css';

const rootElement = document.getElementById('root')

ReactDOM.render(
  <Provider store={store}>
    <AppContainer />
  </Provider>,
  rootElement
)