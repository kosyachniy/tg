import React from 'react';
// import openSocket from 'socket.io-client';
import api from '../../func/api';

// import { socket } from '../../sets';
import './style.css';


const colors = ['192a56', '00b894', 'ffeaa7', 'fab1a0', 'd63031'];
// const colors = ['002593', '007199', '009a5e', '008f18', '009f00', '139500', '89d500', '89d500', 'ffd202', 'e29500', 'ce7100', 'b74e00', '952700'];


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
			const heatmap = res.result.heatmap;
			this.setState({ table: heatmap.result, topics: heatmap.topics })
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

	// 102
	// 153
	// `rgba(${256 * el}, 0, ${256 * (1 - el)})`
	// 0 0.25 0.5 0.75 1

	render() {
		return (
			<>
				<br />
				<table>
					<tbody>
						{ this.state.table.map((el, ind) => (
							<tr key={ind}>
								<td>{ this.state.topics[ind] }</td>
								<td style={{
									backgroundColor: `#${colors[Math.round(el * (colors.length - 1))]}`,
									color: el < 0.3 ? '#fff' : '#000',
								}}>{ Math.round(el * 100) }%</td>
							</tr>
						))}
					</tbody>
				</table>
			</>
		)
	}
}