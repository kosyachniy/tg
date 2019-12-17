from func.tg_user import search_global
from api._func import check_params
from api.get_discuss import get_styled
from api.visualisation import timeline

# Получение

def get(this, **x):
	# Проверка параметров

	check_params(x, (
		('search', True, str),
	))

	# Обработка

	messages = search_global(x['search'], 100)
	posts = get_styled(messages)
	graph = timeline(messages)

	# Ответ

	res = {
		'posts': posts,
		'graph': graph,
	}

	# this.socketio.emit('trends', res, namespace='/main')

	return res