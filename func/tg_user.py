from telethon import TelegramClient, sync
import json

with open('keys.json', 'r') as file:
	keys = json.loads(file.read())

client = TelegramClient('test', keys['tg_app_id'], keys['tg_app_hash']).start()