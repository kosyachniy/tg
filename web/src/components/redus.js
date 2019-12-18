import { combineReducers, createStore } from 'redux';

// actions.js
export const changePath = path => ({
	type: 'CHANGE_PATH',
	path,
});

// reducers.js
export const system = (state = [], action) => {
	switch (action.type) {
		case 'CHANGE_PATH':
			return {path: action.path}

		default:
			return {path: 'heatmap'};
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
