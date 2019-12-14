import React from 'react'
import { Route, Switch } from 'react-router-dom'

import Heatmap from '../../Heatmap'

import './style.css'


export default function Body() {
	return (
		<div class="container" id="main">
			<Switch>
				<Route exact path="/">
					<Heatmap />
				</Route>
			</Switch>
		</div>
	)
}