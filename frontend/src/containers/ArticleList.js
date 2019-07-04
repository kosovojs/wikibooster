import { connect } from 'react-redux';
import ArticleList from '../components/articleList';
import {setArticle} from '../actions/tasks';

const mapStateToProps = (state) => ({
	articles: state.tasks.articles,
	articleId: state.tasks.currentArticle.id
});

const mapDispatchToProps = (dispatch) => ({
	selectArticle: (article, key) => {
		dispatch(setArticle({article, key}));
	},
});

export default connect(
	mapStateToProps,
  	mapDispatchToProps
)(ArticleList);