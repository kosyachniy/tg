import { connect } from 'react-redux';
import {
	changeType, search,
} from '../../redus';

import Header from './Header';


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const mapDispatchToProps = {
	changeType, search,
};

const HeaderContainer = connect(
	mapStateToProps,
	mapDispatchToProps,
)(Header);

export default HeaderContainer;
