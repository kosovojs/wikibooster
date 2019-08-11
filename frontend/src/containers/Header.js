import { connect } from 'react-redux';
import Header from '../components/Header';

const mapStateToProps = (state) => ({
	isAuth: state.auth.isAuth,
	username: state.auth.username,
	tasks: state.tasks.description,
	wiki: state.app.wiki,
	wikis: state.app.wikis
});

export default connect(
	mapStateToProps
)(Header);