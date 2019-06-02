import React from 'react';

const ArticleTitle = (title, wiki) => {
	//const linkForURL = 
	//const link = {title}//<a href='https://'+wiki+'.wikipedia.org/wiki/${title}' target='_blank'>{title}</a>;

	return <span><a href={'https://'+wiki+'.wikipedia.org/wiki/'+title} target='_blank' rel="noopener noreferrer">{title}</a> <small>(<a href={'https://'+wiki+'.wikipedia.org/wiki/'+title} target='_blank' rel="noopener noreferrer">diskusija</a> | <a href={'https://'+wiki+'.wikipedia.org/wiki/'+title} target='_blank' rel="noopener noreferrer">vēsture</a>)</small></span>;
};

export default ArticleTitle;