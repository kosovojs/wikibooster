import React, { Component } from 'react';

export default class ArticleList extends Component {
	
  	render() {
		const {articles, articleId} = this.props;

		return <div id="articleList">
			<div id="articleListTitle"><h3>Rakstu saraksts</h3></div>
				{articles.length>0 ? articles.map((article, key) => <div key={key} onClick={this.props.handleArticleSelect(article, key)} className={articleId === key ? "currentArticle" : "articleItem"}>{article}</div>) : ""}
			</div>;
	}
}