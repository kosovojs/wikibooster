import React from 'react';

const urlSafeTitle = (title) => {
	return encodeURI(title.replace(/ /gi, '_'))
};

const ArticleTitle = (title, wiki) => {
	
	wiki = wiki && wiki.replace('wiki', '')

	const urlSafeWikititle = urlSafeTitle(title);
	
	return <span>
		<a href={'https://' + wiki + '.wikipedia.org/wiki/' + urlSafeWikititle} target='_blank' rel="noopener noreferrer">{title}</a> <span style={{fontSize:'50%'}}>(
			<a href={'https://' + wiki + '.wikipedia.org/w/index.php?title=' + urlSafeWikititle+'&action=edit'} target='_blank' rel="noopener noreferrer">edit</a>
			{' '}|{' '}
			<a href={'https://' + wiki + '.wikipedia.org/w/index.php?title=' + urlSafeWikititle+'&action=history'} target='_blank' rel="noopener noreferrer">history</a>
		)</span>
	</span>;
};

export default ArticleTitle;