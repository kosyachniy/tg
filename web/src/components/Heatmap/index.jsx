import { connect } from 'react-redux';
import Heatmap from './Heatmap'


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const HeatmapContainer = connect(
	mapStateToProps,
)(Heatmap);

export default HeatmapContainer;
