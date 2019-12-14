import time

from mongodb import db
from api._error import ErrorInvalid
from api._func import check_params, next_id

from api.search import search


# Получение

def analytics(this, **x):
	# Проверка параметров

	check_params(x, (
		('tags', True, (str, list), str),
	))

	if type(x['tags']) == str:
		x['tags'] = [x['tags']]

	# Сохранение

	discussion_id = next_id('discussions')

	discussion = {
		'id': discussion_id,
		'tags': x['tags'],
		'time': this.timestamp,
		'user': this.token,
	}

	db['discussions'].insert_one(discussion)

	# Обработка

	search(discussion_id)

	# Ответ

	res = {
		'id': discussion_id,
	}

	return res