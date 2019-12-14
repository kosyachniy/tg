from app import app, sio
from flask import request

import os
import time
import re

from func.tg_user import search_global
from api.get_discuss import get_styled
from api.visualisation import timeline


# Socket.IO

from threading import Lock
from flask_socketio import emit

thread = None
thread_lock = Lock()


# Онлайн пользователи

@sio.on('trends', namespace='/main')
def trends(x):
	# global thread
	# with thread_lock:
	# 	if thread is None:
	# 		thread = sio.start_background_task(target=background_thread)

	sid = request.sid

	print('!1')
	messages = search_global(x['search'], 100)
	print('!2')
	posts = get_styled(messages)
	print('!3')
	graph = timeline(messages)
	print('!4')

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
