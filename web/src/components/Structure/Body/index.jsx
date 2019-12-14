import React from 'react'
import { Route, Switch } from 'react-router-dom'

import Heatmap from '../../Heatmap'
import Trends from '../../Trends'

import './style.css'


export default function Body() {
	return (
		<div className="container" id="main">
			<Switch>
				<Route exact path="/">
					<Heatmap />
				</Route>

				<Route path="/trends">
					<Trends />
				</Route>
			</Switch>
		</div>
	)
}