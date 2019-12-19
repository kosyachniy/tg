import React from 'react';
import { Link, Redirect } from 'react-router-dom';
import api from '../../func/api';

import openSocket from 'socket.io-client';
import { socket } from '../../sets';

import './style.css';


export default class Search extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			search: '',
			submit: false,
			list: [],
			failed: [],
		}

		this.socketIO = null;
	}

	componentWillMount() {
		const handlerSuccess = (that, res) => {
			this.setState({ list: res.result.heatmaps, failed: res.result.failed, });
		};

		api(this, 'heatmap.gets', {}, handlerSuccess);

		this.socketIO = openSocket(`${socket.link}main`);
	}

	render() {
		if (this.state.submit) {
			return (
				<Redirect to={`/${this.props.system.type}/${this.state.search}`} />
			)
		}

		return (
			<>
				{ this.props.system.type === 'heatmap' && (
					<p>Добавить на обработку:</p>
				)}
				<input
					className="form-control mr-sm-2"
					type="search"
					value={this.state.search}
					placeholder={ this.props.system.type === 'heatmap' ? "Ключевое слово" : "Поиск" }
					onChange={(event) => {this.setState({ search: event.target.value })}}
					onKeyDown={(event) => {
						if (event.key === 'Enter' && this.state.search.length > 0) {
							if (this.props.system.type === 'heatmap') {
								this.socketIO.emit('heatmap', {tags: this.state.search, token: localStorage.getItem('token')});
								this.setState({ search: '' })
							} else {
								this.props.search(this.state.search);
								this.setState({ submit: true });
							}
						}
					}}
				/>

				{ (this.props.system.type === 'heatmap' && this.state.list) && (
					<>
						<br />
						<p>Обработанные запросы:</p>
						<ul>
							{ this.state.list.map((el) => (
								<li key={el.id}>
									<Link
										to={`/${this.props.system.type}/${el.tags[0]}`}
										onClick={()=>{this.props.search(el.tags[0])}}
									>
										{ el.tags[0] }
									</Link>
								</li>
							))}
						</ul>
					</>
				)}

				{ (this.props.system.type === 'heatmap' && this.state.failed && this.state.failed.length > 0) && (
					<>
						<br />
						<p>Запросы, сложные для обработки:</p>
						<ul>
							{ this.state.failed.map((el) => (
								<li key={el.id}>
									{ el.tags[0] }
								</li>
							))}
						</ul>
					</>
				)}
			</>
		)
	}
}