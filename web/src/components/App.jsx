import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import { store } from './redus'
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
			<Provider store={store}>
				<BrowserRouter>
					<Header />
					<Body />
				</BrowserRouter>
			</Provider>
		)
	}
}