import React from 'react'
import { Link, Redirect } from 'react-router-dom'

import './style.css'
import { name } from '../../../sets'


export default class Header extends React.Component {
	state = {
		submit: false,
		search: '',
		type: document.location.pathname.split('/')[1],
	}

	render() {
		if (this.state.submit) {
			return (
				<Redirect to={`/${this.state.type}/${this.state.search}`} />
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
								<Link to="/heatmap" className="nav-link" onClick={ () => {this.setState({ type: 'heatmap' })} }>Тепловая карта</Link>
							</li>
							<li className="nav-item dropdown">
								<Link to="/trends" className="nav-link" onClick={ () => {this.setState({ type: 'trends' })} }>Активность</Link>
							</li>
						</ul>
						{ this.state.type === 'trends' && (
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