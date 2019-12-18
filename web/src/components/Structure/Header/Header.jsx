import React from 'react'
import { Link, Redirect } from 'react-router-dom'

import './style.css'
import { name } from '../../../sets'


export default class Header extends React.Component {
	state = {
		submit: false,
		search: '',
		// type: document.location.pathname.split('/')[1],
	}

	componentWillMount() {
		const type = document.location.pathname.split('/')[1];
		this.props.changePath(type);
	}

	changePath = (path) => {
		// this.setState({ type: path });
		this.props.changePath(path);
	}

	render() {
		if (this.state.submit) {
			return (
				<Redirect to={`/${this.props.system.path}/${this.state.search}`} />
			)
		}

		return (
			<nav className="navbar navbar-expand-md navbar-light bg-light sticky-top">
				<div className="container">
					<Link to="/" className="navbar-brand">{ name }</Link>
					<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>

					<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
						<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
							<li className="nav-item dropdown">
								<Link to="/heatmap" className="nav-link" onClick={ () => {this.changePath('heatmap')} }>Тепловая карта</Link>
							</li>
							<li className="nav-item dropdown">
								<Link to="/trends" className="nav-link" onClick={ () => {this.changePath('trends')} }>Активность</Link>
							</li>
						</ul>
						{ this.props.system.path === 'trends' && (
							<ul className="nav navbar-nav navbar-right">
								<li className="nav-item">
									<input
										className="form-control mr-sm-2"
										type="search"
										placeholder="Поиск"
										onChange={(event) => {this.setState({ search: event.target.value })}}
										onKeyDown={(event) => {
											if (event.key === 'Enter' && this.state.search.length > 0) {
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