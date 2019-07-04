import { connect } from 'react-redux';
import Header from '../components/Header';

const mapStateToProps = (state) => ({
	isAuth: state.auth.isAuth,
	username: state.auth.username,
	tasks: state.tasks.description
});

export default connect(
	mapStateToProps
)(Header);