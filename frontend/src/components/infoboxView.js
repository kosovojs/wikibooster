import React from 'react'

const InfoboxView = (props) => {
	const {lv, en} = props;
	return (
		<div style={{display:'flex'}}>
			<textarea style={{width:'50%'}}>{lv}</textarea>
			<textarea style={{width:'50%'}}>{en}</textarea>
		</div>
	)
};

export default InfoboxView;