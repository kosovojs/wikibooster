import React from 'react';

const ArticleTitle = (title, wiki) => {
	//const linkForURL = 
	//const link = {title}//<a href='https://'+wiki+'.wikipedia.org/wiki/${title}' target='_blank'>{title}</a>;

	// <small>(<a href={'https://'+wiki+'.wikipedia.org/wiki/'+title} target='_blank' rel="noopener noreferrer">diskusija</a> | <a href={'https://'+wiki+'.wikipedia.org/wiki/'+title} target='_blank' rel="noopener noreferrer">vēsture</a>)</small>
	wiki = wiki && wiki.replace('wiki','')
	return <span><a href={'https://'+wiki+'.wikipedia.org/wiki/'+title} target='_blank' rel="noopener noreferrer">{title}</a></span>;
};

export default ArticleTitle;