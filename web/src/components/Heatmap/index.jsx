import React from 'react';
import openSocket from 'socket.io-client';

import { socket } from '../../sets';
import './style.css';


export default class Heatmap extends React.Component {
	state = {
		search: decodeURIComponent(document.location.pathname.split('/')[2]),
		loading: true,
		progress: 0,
		table: [],
	}

	componentWillMount() {
		const socketIO = openSocket(`${socket.link}main`);

		socketIO.emit('heatmap', {tags: this.state.search, token: localStorage.getItem('token')})

		socketIO.on('heatmap', (res) => {
			this.setState({ loading: false, posts: res.posts, graph: res.graph });
		})
	}

	componentDidMount() {
		this.setState({ progress: 0 })
	}

	componentDidUpdate() {
		if (this.state.loading && this.state.progress < 100) {
			setTimeout(() => {
				let progress = Math.min(this.state.progress + 0.67, 100)
				this.setState({ progress })
			}, 100)
		}
	}

	render() {
		if (this.state.loading) {
			return (
				<>
					<br /><br />

					Загрузка.. ({ Math.round(this.state.progress) }%)
					<div className="progress">
						<div className="progress-bar bg-warning" role="progressbar" style={ {width: `${this.state.progress}%`} } aria-valuenow={this.state.progress} aria-valuemin="0" aria-valuemax="100"></div>
					</div>
				</>
			)
		}

		return (
			<>
				<br /><hr /><br />


			</>
		)
	}
}