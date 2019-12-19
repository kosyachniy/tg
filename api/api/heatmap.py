from urllib.request import unquote

from mongodb import db
from api._error import ErrorInvalid, ErrorWrong
from api._func import check_params, next_id

from api.search import search


# Список
def gets(this, **x):
	db_filter = {
		'_id': False,
		'id': True,
		'tags': True,
		'time': True,
	}
	heatmaps = list(db['discussions'].find({'status': 5}, db_filter).sort('time', -1))

	# Неудачные

	failed = list(db['discussions'].find({'status': 4}, db_filter).sort('time', -1))

	# Ответ

	res = {
		'heatmaps': heatmaps,
		'failed': failed,
	}

	return res

# Получение

def get(this, **x):
	db_condition = {
		'tags': [unquote(x['tag'])],
		'status': 5,
	}
	db_filter = {
		'_id': False,
		'id': True,
		'tags': True,
		'topics': True,
		'timeline': True,
		'result': True,
	}
	heatmap = db['discussions'].find_one(db_condition, db_filter)

	if not heatmap:
		raise ErrorWrong('tag')

	# Обработка

	heatmap['result'] = list(map(lambda y: list(map(lambda x: round(x, 4), y)), heatmap['result']))

	# Ответ

	res = {
		'heatmap': heatmap,
	}

	return res

# def get(this, **x):
# 	# Проверка параметров

# 	check_params(x, (
# 		('tags', True, (str, list), str),
# 	))

# 	if type(x['tags']) == str:
# 		x['tags'] = [x['tags']]

# 	# Сохранение

# 	discussion_id = next_id('discussions')

# 	discussion = {
# 		'id': discussion_id,
# 		'tags': x['tags'],
# 		'time': this.timestamp,
# 		'user': this.token,
# 	}

# 	db['discussions'].insert_one(discussion)

# 	# Обработка

# 	search(discussion_id)

# 	# Ответ

# 	res = {
# 		'id': discussion_id,
# 	}

# 	return res