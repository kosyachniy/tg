import time

from mongodb import db
import api._error as Error
from api._func import get_language

import api.discussions as discussions


class API():
	def __init__(self, server, client, token): # ip, socketio=None, language=0, ip_remote=None):
		self.timestamp = time.time()
		self.server = server
		self.client = client
		# self.socketio = socketio
		# self.ip = ip
		self.token = token
		# self.language = language

		# # Язык

		# self.language = get_language(self.language)

		# # Определение пользователя

		# self.user = {
		# 	'id': 0,
		# 	'admin': 2,
		# }

		# if token:
		# 	db_filter = {'id': True, '_id': False}
		# 	user_id = db['tokens'].find_one({'token': token}, db_filter)
		# 	if user_id and user_id['id']:
		# 		self.user = db['users'].find_one({'id': user_id['id']})
		
		# # IP (случай, когда Веб-приложение делает запросы к IP с того же адреса)

		# if ip_remote and ip == self.client['ip']:
		# 	self.ip = ip_remote

	def method(self, name, params={}):
		# Убираем лишние отступы

		for i in params:
			if type(params[i]) == str:
				params[i] = params[i].strip()

		# Отслеживание действий

		req = {
			'time': self.timestamp,
			'user': self.token, # self.user['id'],
			# 'ip': self.ip,
			'method': name,
			'params': params,
		}

		db['actions'].insert(req)
	
		# Метод API

		try:
			module, method = name.split('.')
			func = getattr(globals()[module], method)
		except:
			raise Error.ErrorWrong('method')
		
		# Запрос

		return func(self, **params)