import { combineReducers, createStore } from 'redux';

// actions.js
export const changeType = path => ({
	type: 'CHANGE_TYPE',
	path,
});

export const search = request => ({
	type: 'SEARCH',
	request,
});

// reducers.js
export const system = (state = [], action) => {
	switch (action.type) {
		case 'CHANGE_TYPE':
			return {...state, type: action.path}

		case 'SEARCH':
			return {...state, search: action.request}

		default:
			return {type: 'heatmap', search: ''};
	}
};


export const reducers = combineReducers({
	system,
});

// store.js
export function configureStore(initialState = {}) {
	const store = createStore(reducers, initialState);
	return store;
}

export const store = configureStore();
