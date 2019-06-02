import React, { Component } from 'react';
//import WikEdDiff from '../WikEdDiff';
let WikEdDiff = require('../WikEdDiff');

const Comparision = (orig, changed) => {
	let wpDiff = WikEdDiff.WikEdDiff;
	let diff1 = new wpDiff();
	const diff = diff1.diff(orig, changed);

	return <div dangerouslySetInnerHTML={{__html: diff}} />
};

export default Comparision;