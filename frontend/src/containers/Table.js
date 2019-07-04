import { connect } from 'react-redux';
import { setTableData, updateRow, removeRow } from '../actions/table';
import {setVisibilityFilter} from '../actions/visibilityFilters';
import Table from '../components/Table';

const getVisibleRows = (rows, filters) => {
	return rows
		.filter(row => filters.targetLanguage === '' || row[1] === null || row[1].toLowerCase().includes(filters.targetLanguage.toLowerCase()))
		.filter(row => filters.originalLanguage === '' || row[2] === null || row[2].toLowerCase().includes(filters.originalLanguage.toLowerCase()))
};

const mapStateToProps = (state) => ({
  rows: getVisibleRows(state.table.rows, state.visibilityFilter)
})

const mapDispatchToProps = (dispatch) => ({
  onDataLoad: () => dispatch(setTableData()),
  onRowUpdate: ({newData, oldData}) => dispatch(updateRow({newData, oldData})),
  onRowRemove: (oldData) => dispatch(removeRow(oldData)),

  setFilter: ({key, filter}) => dispatch(setVisibilityFilter({key, filter}))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Table);