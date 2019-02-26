import sys
import json
import datetime

from telethon import TelegramClient, sync
from telethon.tl.types import InputPeerEmpty # , Channel, Chat, User, InputUserEmpty, InputPeerSelf, InputMessagesFilterEmpty
from telethon.tl.functions.messages import SearchGlobalRequest # , SearchRequest, GetFullChatRequest
# from telethon.tl.functions.channels import GetFullChannelRequest
# from telethon.tl.functions.users import GetFullUserRequest


with open('keys.json', 'r') as file:
	keys = json.loads(file.read())

client = TelegramClient('main', keys['tg_app_id'], keys['tg_app_hash']).start()


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
	return client.get_entity(name)

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

# Поиск

def search(text, count=None, mes_author=None, mes_type=None):
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


if __name__ == '__main__':
	if len(sys.argv) > 2:
		res = globals()[sys.argv[1]](*sys.argv[2:])
	else:
		res = globals()[sys.argv[1]]()

	print(res)