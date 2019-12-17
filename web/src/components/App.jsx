import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.min.js'

import Header from './Structure/Header'
import Body from './Structure/Body'


function genereteToken() {
    const res = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    return res.substr(0, 32);
}

export default class App extends React.Component {
	componentWillMount() {
		localStorage.setItem('token', genereteToken())
	}

	render() {
		return (
			<BrowserRouter>
				<Header />
				<Body />
			</BrowserRouter>
		)
	}
}