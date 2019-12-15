import sys
import json
import datetime
import time

import re
from telethon import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputMessagesFilterEmpty # , Channel, Chat, User, InputUserEmpty, InputPeerSelf, InputMessagesFilterEmpty
from telethon.tl.functions.messages import SearchGlobalRequest, SearchRequest # , GetFullChatRequest
# from telethon.tl.functions.channels import GetFullChannelRequest
# from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest

from keys import TG
from sets import CHATS


client = TelegramClient('main', TG['app_id'], TG['app_hash']).start()


# Текущий аккаунт

def get_me():
	return client.get_me()

# # Список диалогов

# # None - вся история
# def get_dialogs(count=None):
# 	dialogs = []

# 	for i in client.get_dialogs()[:count]:
# 		entity = i.entity.to_dict()

# 		res = {
# 			'id': entity['id'],
# 			'type': entity['_'],
# 			'username': entity['username'] if 'username' in entity else None,
# 		}
# 		if entity['_'] == 'User':
# 			res['access'] = entity['access_hash']
# 			res['bot'] = entity['bot']
# 			res['name'] = entity['first_name']
# 			res['surname'] = entity['last_name']
# 		elif entity['_'] == 'Channel':
# 			res['access'] = entity['access_hash']
# 			res['title'] = entity['title']
# 			res['super'] = entity['megagroup']
# 		elif entity['_'] == 'Chat':
# 			res['title'] = entity['title']

# 		dialogs.append(res)

# 	return '\n'.join([str(i) for i in dialogs])

# Получить сущность

# 't.me/nickname' / '@nickname' / id
def get_entity(name):
	def convert(cont):
		try:
			return int(cont)
		except:
			return cont

	return client.get_entity(convert(name))

# # История сообщений

# def get_messages(id):
# 	return client.get_message_history(id)

# # Полная информация

# def get_full(name):
# 	entity = client.get_entity(name)
# 	print(entity)

# 	if type(entity) == Channel:
# 		full = GetFullChannelRequest(entity)
# 	elif type(entity) == Chat:
# 		full = GetFullChatRequest(entity)
# 	elif type(entity) == User:
# 		full = GetFullUserRequest(entity)
# 	else:
# 		raise AssertionError(entity)

# 	return full.to_dict()

# Список крупных чатов

def only_chats():
	chats = []

	for i in client.get_dialogs():
		entity = i.entity.to_dict()


		if (entity['_'] == 'Channel' and entity['megagroup']): # or (entity['_'] == 'Chat'):
			res = {
				'id': entity['id'],
				'type': entity['_'],
				'username': entity['username'] if 'username' in entity else None,
				'title': entity['title'],
				'members': client(GetFullChannelRequest(channel=get_entity(entity['id']))).full_chat.participants_count,
			}

			chat = {
				'channel_id': res['id'],
				'access_hash': entity['access_hash'],
			}

			print(res)
			
			if res['members'] > 500:
				chats.append(chat)

	return chats

# Поиск

def search(text, count=100, mes_author=None, mes_type=None):
	count = int(count)
	re_count = count + 0
	messages = []

	for chat in CHATS:
		# print('!1', chat)
		count = re_count + 0
		offset = 0
		while True:
			count_new = 100 if not count else min(100, count)

			# messages_new = client(SearchGlobalRequest(
			# 	q=text,
			# 	offset_date=datetime.datetime.now(),
			# 	offset_peer=InputPeerChannel(**chat), # InputPeerEmpty(),
			# 	offset_id=offset,
			# 	limit=count_new,
			# )).messages

			messages_new = client(SearchRequest(
				peer=chat['channel_id'],
				q=text,
				filter=InputMessagesFilterEmpty(),
				min_date=datetime.datetime(2017, 1, 1),
				max_date=datetime.datetime(2019, 12, 30),
				offset_id=offset,
				add_offset=0,
				max_id=0,
				min_id=0,
				hash=0, # chat['access_hash'],
				limit=count_new,
			)).messages

			messages.extend(messages_new)

			if count:
				count -= count_new

			if len(messages_new) < 100 or count == 0:
				break

			offset += 100

	return messages

# Глобальный поиск

def search_global(text, count=100, mes_author=None, mes_type=None):
	count = int(count)
	messages = []

	if not count or count > 100:
		offset = 0
		while True:
			count_new = 100 if not count else min(100, count)

			messages_new = client(SearchGlobalRequest(
				q=text,
				offset_date=datetime.datetime.now(),
				offset_peer=InputPeerEmpty(),
				offset_id=offset,
				limit=count_new,
			)).messages

			messages.extend(messages_new)

			if count:
				count -= count_new

			if len(messages_new) < 100 or count == 0:
				break

			offset += 100

	else:
		messages = client(SearchGlobalRequest(
			q=text,
			offset_date=datetime.datetime.now(),
			offset_peer=InputPeerEmpty(),
			offset_id=0,
			limit=count,
		)).messages

	return messages

#

def mes2json(source, message, param_source=True):
	req = {
		'id': message.id,
		'time': int(message.date.timestamp()),
	}

	if message.message:
		req['body'] = message.message

		if message.mentioned:
			mentions = [{'id': get_entity(i).id} for i in re.findall(r'@[0-9_]*[a-zA-Z_]+[0-9_]*', message.message)]

			if mentions:
				req['mentions'] = mentions

	else:
		req['body'] = ''
	
	if message.from_id:
		req['author'] = {'id': message.from_id}

	if param_source:
		req['source'] = {'id': source}

	if message.views:
		req['reactions'] = {'views': {'count': message.views}}

	return req

def history(name, limit=100):
	source = get_entity(name).id
	processor = lambda message: mes2json(source, message, False)

	messages = []
	iteration = 0

	while True:
		messages.extend(map(processor, client.get_messages(source, limit=limit, add_offset=iteration * limit)))

		iteration += 1

		if len(messages) != iteration * limit:
			break
	
		print(len(messages))
		time.sleep(1) #
	
	return messages[::-1]

def dialogs():
	return [i.id for i in client.get_dialogs()]


if __name__ == '__main__':
	if len(sys.argv) > 2:
		res = globals()[sys.argv[1]](*sys.argv[2:])
	else:
		res = globals()[sys.argv[1]]()

	print(res)