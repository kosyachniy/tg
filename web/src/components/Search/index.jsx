import { connect } from 'react-redux';
import {
	search,
} from '../redus';

import Search from './Search'


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const mapDispatchToProps = {
	search,
};

const SearchContainer = connect(
	mapStateToProps,
	mapDispatchToProps,
)(Search);

export default SearchContainer;
