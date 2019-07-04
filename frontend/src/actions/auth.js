import {urlendpoint} from '../config';

export const LOGIN = 'LOGIN';
export const LOGOUT = 'LOGOUT';

export const login = (username) => ({
	type: LOGIN,
	username
});

export const logout = () => ({
	type: LOGOUT
});

export const checkAuth = () => {
	return function(dispatch) {
	  return fetch(`${urlendpoint}info`)
			.then(
				response => response.json(),
				error => console.log('An error occurred.', error)
			)
			.then(json => {
				if (json.status === 'ok') {
					dispatch(login(json.username));
				}
			}
		)
	}
}
