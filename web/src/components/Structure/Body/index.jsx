import React from 'react'
import { Route, Switch, Redirect } from 'react-router-dom'

import Heatmap from '../../Heatmap'
import Trends from '../../Trends'
import Search from '../../Search'

import './style.css'


export default function Body() {
	return (
		<div className="container" id="main">
			<Switch>
				<Route exact path="/">
					<Redirect to="/heatmap" />
				</Route>

				<Route path="/heatmap" exact>
					<Search
						type="heatmap"
					/>
				</Route>

				<Route path="/heatmap/:search">
					<Heatmap />
				</Route>

				<Route path="/trends" exact>
					<Search
						type="trends"
					/>
				</Route>

				<Route path="/trends/:search">
					<Trends />
				</Route>
			</Switch>
		</div>
	)
}