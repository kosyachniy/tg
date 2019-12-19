import React from 'react';
// import openSocket from 'socket.io-client';
import api from '../../func/api';

// import { socket } from '../../sets';
import './style.css';


export default class Heatmap extends React.Component {
	state = {
		// search: decodeURIComponent(document.location.pathname.split('/')[2]),
		loading: true,
		progress: 0,
		table: [],
	}

	componentWillMount() {
		// const socketIO = openSocket(`${socket.link}main`);

		// socketIO.emit('heatmap', {tags: this.state.search, token: localStorage.getItem('token')})

		// socketIO.on('heatmap', (res) => {
		// 	this.setState({ loading: false, posts: res.posts, graph: res.graph });
		// })

		const handleSuccess = (that, res) => {
			const heatmap = res.result.heatmap.result;
			console.log('HEAT', Object.keys(heatmap), Object.keys(heatmap).map(key => {console.log(heatmap[key])}))
		}

		api(this, 'heatmap.get', {tag: this.props.system.search}, handleSuccess)
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
		return (
			<>
				<br /><hr /><br />


			</>
		)
	}
}