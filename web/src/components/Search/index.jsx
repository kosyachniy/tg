import { connect } from 'react-redux';
import Search from './Search'


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const SearchContainer = connect(
	mapStateToProps,
)(Search);

export default SearchContainer;
