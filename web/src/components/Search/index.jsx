import React from 'react';
import { Redirect } from 'react-router-dom';

import './style.css';


export default class Search extends React.Component {
	state = {
		search: '',
		submit: false,
		type: this.props.type,
		// type: document.location.pathname.split('/')[1],
	}

	render() {
		console.log(this.state)
		if (this.state.submit) {
			return (
				<Redirect to={`/${this.state.type}/${this.state.search}`} />
			)
		}

		return (
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
		)
	}
}