from telethon import TelegramClient, sync

import json


with open('keys.json', 'r') as file:
	keys = json.loads(file.read())

client = TelegramClient('test2', keys['tg_app_id'], keys['tg_app_hash']).start()
# client.connect()

# if not client.is_user_authorized():
# 	client.send_code_request(x['phone'])
# 	client.sign_in(x['phone'], input('Код: '))