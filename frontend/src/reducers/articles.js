import { SET_TABLE_DATA, UPDATE_ROW, REMOVE_ROW } from '../actions/table';
import {data} from '../fakeJson';

const defaultState = {
	rows: []
};
const table = (state = defaultState, action) => {
  switch (action.type) {
    case SET_TABLE_DATA: {
		//const {language, rows123} = action;
		
		const rows = data;
		
		return Object.assign({},{rows});
	}
    case UPDATE_ROW: {
		const {newData} = action;
		
		const wd = newData[0];
		const lv = newData[1];
		const en = newData[2];
		
		return {
			...state,
			rows: state.rows.map( row => row[0] === wd ? [wd,lv,en] : row)
		};
	}
    case REMOVE_ROW: {
		const {oldData} = action;
		
		const wd = oldData[0];
		
		return {
			...state,
			rows: state.rows.filter( row => row[0] !== wd)
		};
	}
    default:
      return state
  }
};

export default table;