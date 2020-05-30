import React from 'react'
import { Link, Redirect } from 'react-router-dom'

import './style.css'
import { name } from '../../../sets'


export default class Header extends React.Component {
	state = {
		submit: false,
		search: '',
	}

	componentWillMount() {
		const path = document.location.pathname.split('/');

		const type = path.length > 1 && path[1] && path[1].length > 0 ? path[1] : 'heatmap';
		this.props.changeType(type);

		const request = path.length > 2 ? path[2] : '';
		this.props.search(request);
	}

	changeType = (path) => {
		// this.setState({ type: path });
		this.props.changeType(path);
		this.props.search('');
	}

	render() {
		const { type, search } = this.props.system;
		console.log(type, search);

		if (this.state.submit) {
			console.log('REDIRECT')
			return (
				<Redirect to={`/${type}/${this.props.system.search}`} />
			)
		}

		return (
			<nav className="navbar navbar-expand-md navbar-light bg-light sticky-top">
				<div className="container">
					<Link to="/" className="navbar-brand" onClick={ () => {this.changeType('heatmap')} }>{ name }</Link>
					<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>

					<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
						<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
							<li className="nav-item dropdown">
								<Link to="/heatmap" className="nav-link" onClick={ () => {this.changeType('heatmap')} }>Тепловая карта</Link>
							</li>
							<li className="nav-item dropdown">
								<Link to="/trends" className="nav-link" onClick={ () => {this.changeType('trends')} }>Активность</Link>
							</li>
						</ul>
						{ (type === 'trends' && search.length > 0) && (
							<ul className="nav navbar-nav navbar-right">
								<li className="nav-item">
									<input
										className="form-control mr-sm-2"
										type="search"
										placeholder="Поиск"
										onChange={(event) => {this.setState({ search: event.target.value })}}
										onKeyDown={(event) => {
											if (event.key === 'Enter' && this.state.search.length > 0) {
												console.log('!CHECK!')
												this.props.search(this.state.search);
												this.setState({ submit: true });
											}
										}}
									/>
								</li>
							</ul>
						) }
					</div>
				</div>
			</nav>
		)
	}
}