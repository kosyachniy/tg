import React from 'react'
import { Link } from 'react-router-dom'

import './style.css'
import { name } from '../../../sets'


export default function Header() {
	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top">
			<div className="container">
				<a className="navbar-brand">{ name }</a>
				<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span className="navbar-toggler-icon"></span>
				</button>

				<div className="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul className="navbar-nav mr-auto mt-2 mt-lg-0">
						<li className="nav-item dropdown">
							<Link to="/" className="nav-link">Тепловая карта</Link>
						</li>
						<li className="nav-item dropdown">
							<Link to="/trends" className="nav-link">Активность</Link>
						</li>
					</ul>
					<ul className="nav navbar-nav navbar-right">
						<li className="nav-item">	
							<form action="/sys_search/" method="post" className="form-inline my-2 my-lg-0">
								<input name="search" className="form-control mr-sm-2" type="search" placeholder="Search" />
							</form>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	)
}