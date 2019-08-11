import React from 'react';

export default function ArticleList({articles, articleId, selectArticle}) {
	return <div id="articleList">
	<div id="articleListTitle"><h3>Article list</h3></div>
		{articles.length>0 ? articles.map((article, key) => <div key={key} onClick={() => selectArticle(article, key)} className={articleId === key ? "currentArticle" : "articleItem"}>{article}</div>) : ""}
	</div>;
};