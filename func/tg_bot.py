import telegram
import json
import time
from telegram.error import NetworkError, Unauthorized


def process(echo):
	with open('keys.json', 'r') as file:
		TOKEN = json.loads(file.read())['tg_token']

	bot = telegram.Bot(token=TOKEN)

	try:
		update_id = bot.get_updates()[0].update_id
	except IndexError:
		update_id = None

	while True:
		try:
			for update in bot.get_updates(offset=update_id, timeout=10):
				update_id = update.update_id + 1

				if update.message:
					echo(update)

		except NetworkError:
			time.sleep(1)

		except Unauthorized:
			update_id += 1