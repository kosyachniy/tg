import { connect } from 'react-redux';
import {
	changePath,
} from '../../redus';

import Header from './Header';


// AppContainer.jsx
const mapStateToProps = state => ({
	system: state.system,
});

const mapDispatchToProps = {
	changePath,
};

const HeaderContainer = connect(
	mapStateToProps,
	mapDispatchToProps,
)(Header);

export default HeaderContainer;
