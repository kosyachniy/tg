import { connect } from 'react-redux';
import Trends from './Trends'


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const TrendsContainer = connect(
	mapStateToProps,
)(Trends);

export default TrendsContainer;
