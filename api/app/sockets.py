from app import app, sio
from flask import request

import time

from mongodb import db
from func.tg_user import search_global
from api._func import next_id
from api.get_discuss import get_styled
from api.visualisation import timeline
from api.vectorize import vectorize
from api.lda import lda
from api.search import search


# Socket.IO

from threading import Lock
from flask_socketio import emit

thread = None
thread_lock = Lock()


# Теплвоая карта


@sio.on('heatmap', namespace='/main')
def heatmap(x):
	# global thread
	# with thread_lock:
	# 	if thread is None:
	# 		thread = sio.start_background_task(target=background_thread)

	sid = request.sid
	timestamp = time.time()

	# Отслеживание

	req = {
		'time': timestamp,
		'user': x['token'],
		'method': 'heatmap',
		'params': {'tags': x['tags']},
	}

	db['actions'].insert_one(req)

	#

	if type(x['tags']) == str:
		x['tags'] = [x['tags']]

	discussion_id = next_id('discussions')

	discussion = {
		'id': discussion_id,
		'tags': x['tags'],
		'time': timestamp,
		'user': x['token'],
		'status': 0,
	}

	db['discussions'].insert_one(discussion)

	# Обработка

	print('HEAT', '1', x['tags'])
	search(discussion_id)
	print('HEAT', '2')

	discussion = db['discussions'].find_one({'id': discussion_id})
	discussion['status'] = 1
	db['discussions'].save(discussion)

	texts, sets, inds, corpus, freq = vectorize(discussion_id)
	for i in range(len(inds)):
		message = db['messages'].find_one({'_id': inds[i]})
		message['preprocessed'] = sets[i]
		db['messages'].save(message)
	print('HEAT', '3', '\nDataset: {}\nCorpus: {}\n'.format(len(sets), len(corpus)))

	discussion = db['discussions'].find_one({'id': discussion_id})
	discussion['status'] = 2
	db['discussions'].save(discussion)

	lda_model, corpus, data_ready, data_inds, topics, prob = lda(discussion_id)
	topics_list = list(map(lambda x: x[1], lda_model.print_topics()))
	discussion = db['discussions'].find_one({'id': discussion_id})
	discussion['topics'] = topics_list
	db['discussions'].save(discussion)
	for i in range(len(data_inds)):
		message = db['messages'].find_one({'_id': data_inds[i]})
		message['topic'] = {
			'name': topics[i],
			'probability': float(round(prob[i], 3)),
		}
		db['messages'].save(message)
	print('HEAT', '4', '\Topics: {}'.format(topics_list))

	discussion = db['discussions'].find_one({'id': discussion_id})
	discussion['status'] = 3
	db['discussions'].save(discussion)

	topics = {i: 0 for i, el in enumerate(discussion['topics'])}

	db_condition = {
		'discussion': discussion_id,
		'topic': {'$exists': True},
	}
	db_filter = {
		'_id': False,
		'topic.name': True,
	}
	messages = [i for i in db['messages'].find(db_condition, db_filter)]

	mes_all = len(messages)

	for message in messages:
		topics[message['topic']['name']] += 1

	discussion['result'] = [topics[i] / mes_all for i in range(len(topics))]
	discussion['status'] = 4
	db['discussions'].save(discussion)

	# # Ответ

	# res = {
	# 	'dataset': len(sets),
	# 	'corpus': len(corpus),
	# 	'topics': topics_list,
	# 	'lda': [],
	# 	'heatmap': [],
	# }

	# sio.emit('heatmap', res, room=sid, namespace='/main')

# Тренды

@sio.on('trends', namespace='/main')
def trends(x):
	# global thread
	# with thread_lock:
	# 	if thread is None:
	# 		thread = sio.start_background_task(target=background_thread)

	sid = request.sid
	timestamp = time.time()

	# Отслеживание

	req = {
		'time': timestamp,
		'user': x['token'],
		'method': 'trends',
		'params': {'search': x['search']},
	}

	#

	print('TREND', '1', x['search'])
	messages = search_global(x['search'], 100)
	print('TREND', '2')
	posts = get_styled(messages)
	print('TREND', '3')
	graph = timeline(messages)
	print('TREND', '4')

	# Ответ

	res = {
		'posts': posts,
		'graph': graph,
	}

	sio.emit('trends', res, room=sid, namespace='/main')

#

if __name__ == '__main__':
	sio.run(app, debug=False, log_output=False)


# def background_thread():
# 	while True:
# 		timestamp = time.time()

#         #

# 		pass

# 		#

# 		time.sleep(1)
