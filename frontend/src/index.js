import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import AppContainer from './containers/App';

import { Provider } from 'react-redux';
import store from './store';

const rootElement = document.getElementById('root')

ReactDOM.render(
  <Provider store={store}>
    <AppContainer />
  </Provider>,
  rootElement
)