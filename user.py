from func.tg_user import client

import datetime

from telethon.tl.types import Channel, Chat, User
from telethon.tl.types import InputMessagesFilterEmpty, InputUserEmpty, InputPeerEmpty, InputPeerSelf
from telethon.tl.functions.messages import SearchRequest, SearchGlobalRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.users import GetFullUserRequest


def get_me():
	return client.get_me()

# Отправить сообщение
def send_message(name='kosyachniy', message='Hello ;)'):
	client.send_message(name, message)

# Список диалогов
# None - вся история
def get_dialogs(count=10):
	dialogs = []

	for i in client.get_dialogs()[:count]:
		entity = i.entity.to_dict()

		res = {
			'id': entity['id'],
			'type': entity['_'],
			'username': entity['username'] if 'username' in entity else None,
		}
		if entity['_'] == 'User':
			res['access'] = entity['access_hash']
			res['bot'] = entity['bot']
			res['name'] = entity['first_name']
			res['surname'] = entity['last_name']
		elif entity['_'] == 'Channel':
			res['access'] = entity['access_hash']
			res['title'] = entity['title']
			res['super'] = entity['megagroup']
		elif entity['_'] == 'Chat':
			res['title'] = entity['title']

		dialogs.append(res)

	return '\n'.join([str(i) for i in dialogs])

# Получить сущность
# 't.me/nickname' / '@nickname' / id
def get_entity(name=1142824902):
	return client.get_entity(name)

# История сообщений
def get_messages(id=136563129):
	return client.get_message_history(id)

# Получение полной информации
def get_full(name=1091219672):
	entity = client.get_entity(name)
	print(entity)

	if type(entity) == Channel:
		full = GetFullChannelRequest(entity)
	elif type(entity) == Chat:
		full = GetFullChatRequest(entity)
	elif type(entity) == User:
		full = GetFullUserRequest(entity)
	else:
		raise AssertionError(entity)

	return full.to_dict()

def search(text='ФИО', name=None):
	if name:
		entity = client.get_entity(name)
	else:
		entity = InputPeerEmpty()

	return client(SearchRequest(
		peer=entity,
		q=text,
		filter=InputMessagesFilterEmpty(),
		min_date=datetime.datetime(2018, 11, 22),
		max_date=None, # datetime.datetime(2018, 11, 23),
		offset_id=0,
		add_offset=0,
		limit=100,
		max_id=0,
		min_id=0,
		hash=0,
		from_id=None, # InputUserEmpty(),
	))

	# return client(SearchGlobalRequest(
	# 	q=text,
	# 	offset_date=datetime.datetime(2018, 11, 23),
	# 	offset_peer=InputPeerSelf(),
	# 	offset_id=0,
	# 	limit=100,
	# ))


# def replier(update):
# 	if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)) and str(update.message.to_id.channel_id) in from_id:
# 		print(update)
# 		text = update.message.message

# 		try:
# 			text += '\n' + update.message.media.caption
# 		except:
# 			pass

# 		print(text)

# client.add_update_handler(replier)
# input('!')
# client.disconnect()

# @client.on(events.NewMessage)
# async def my_event_handler(event):
#	 if 'hello' in event.raw_text:
#		 await event.reply('hi!')

# client.start()
# client.run_until_disconnected()


if __name__ == '__main__':
	# print(get_dialogs())
	# print(get_full(int(input())))
	print(search(input()))