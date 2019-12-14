import React from 'react'

import './style.css'
// import { api } from '../../func/api'


export default class Heatmap extends React.Component {
	state = {
		tags: [],
	}

	componentWillMount() {
	}

	render() {
		return (
			<>
				{ this.state.tags.map(tag => (
					<div className="card">
						<div className="card-body">
							<h5><b>Источник</b> (Источник ID / ID сообщения)</h5>

							<span className="badge badge-success">
								Время
							</span>

							{ tag.views && (
								<span className="badge badge-success">
									Количество просмотров
								</span>
							)}

							<br />
							Содержание
						</div>
					</div>
				))}
			</>
		)
	}
}