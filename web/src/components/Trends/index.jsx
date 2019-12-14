import React from 'react'
import Chart from 'chart.js'

import './style.css'
// import api from '../../func/api'

import openSocket from 'socket.io-client';
import { socket } from '../../sets';
const socketIO = openSocket(`${socket.link}main`);


export default class Trends extends React.Component {
	state = {
		search: 'Керчь',
		loading: true,
		progress: 0,
		posts: [],
		graph: [],
		graphed: false,
	}

	// getTrends = (search) => {
	// 	// const handlerSuccess = (res) => {
	// 	// 	// this.props.notesGet(res['notes']);
	// 	// 	// this.setState({ loadNotes: true });
	// 	// 	this.setState({ posts: res.posts, graph: res.graph });
	// 	// }

	// 	api('trends.get', {search}); // , handlerSuccess);
	// }

	componentWillMount() {
		// this.getTrends(this.state.search);

		socketIO.emit('trends', {search: this.state.search})

		socketIO.on('trends', (res) => {
			// console.log('NICE')
			console.log(res);
			this.setState({ loading: false, posts: res.posts, graph: res.graph });
		})
	}

	componentDidMount() {
		// console.log('DID')
		this.setState({ progress: 0 })
	}

	componentDidUpdate() {
		if (this.state.loading && this.state.progress < 100) {
			setTimeout(() => {
				// console.log('UPD')
				let progress = Math.min(this.state.progress + 0.67, 100)
				this.setState({ progress })
			}, 100)
		}

		if (!this.state.loading && !this.state.graphed) {
			this.setState({ graphed: true });

			let ctx = document.getElementById('chart').getContext('2d');
			console.log('HEY', ctx);
			new Chart(ctx, {
				type: 'line',
				data: {
					labels: this.state.graph.map(function (i) {
						return i.time;
					}),
					datasets: [{
						label: "Обсуждаемость",
						// backgroundColor: 'rgb(255, 204, 0)',
						borderColor: 'rgb(204, 153, 0)',
						data: this.state.graph.map(function (i) {
							return i.count;
						}),
					}],
				},
	
				options: {},
			});
		}
	}

	render() {
		// console.log(this.state.progress)
		if (this.state.loading) {
			return (
				<>
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
				
				<canvas id="chart"></canvas>

				<br /><br />

				<span className="badge badge-primary">
					Сообщений: { this.state.posts.length }
				</span>

				<br /><br /><hr /><br />

				{ this.state.posts.map(post => (
					<div className="card" key={`${post.source.id}/${post.id}`}>
						<div className="card-body">
							<h5><b>{ post.source.name }</b> ({ post.source.id } / { post.id })</h5>

							<span className="badge badge-success">
								{ post.time }
							</span>

							{ post.views && (
								<span className="badge badge-success">
									{ post.views } просмотров
								</span>
							)}

							<br />
							{ post.cont }
						</div>
					</div>
				))}
			</>
		)
	}
}