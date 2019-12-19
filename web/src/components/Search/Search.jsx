import React from 'react';
import { Link, Redirect } from 'react-router-dom';
import api from '../../func/api';

import './style.css';


export default class Search extends React.Component {
	state = {
		search: '',
		submit: false,
		list: [],
	}

	componentWillMount() {
		const handlerSuccess = (that, res) => {
			this.setState({ list: res.result.heatmaps });
		};

		api(this, 'heatmap.gets', {}, handlerSuccess);
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
					placeholder={ this.props.system.type === 'heatmap' ? "Ключевое слово" : "Поиск" }
					onChange={(event) => {this.setState({ search: event.target.value })}}
					onKeyDown={(event) => {
						if (event.key === 'Enter' && this.state.search.length > 0) {
							this.props.search(this.state.search);
							this.setState({ submit: true });
						}
					}}
				/>
				
				{ (this.props.system.type == 'heatmap' && this.state.list) && (
					<>
						<br />
						<p>Обработанные запросы:</p>
						<ul>
							{ this.state.list.map((el) => (
								<li key={el.id}><Link to={`/${this.props.system.type}/${el.tags[0]}`}>{ el.tags[0] }</Link></li>
							))}
						</ul>
					</>
				)}
			</>
		)
	}
}