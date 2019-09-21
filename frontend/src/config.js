export const urlendpoint = (process.env.NODE_ENV === 'development')
    ? '//tools.wmflabs.org/booster/'//'http://127.0.0.1:5000/'
	: '//tools.wmflabs.org/booster/';
//'http://127.0.0.1:5000/'