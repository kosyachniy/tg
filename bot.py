from func.tg_bot import process

@process
def echo(update):
	print('Object Update:', update)

	message = update.message
	user = message.from_user
	print('Object User:', user)

	update.message.reply_text(user.id)

	print('-' * 100)


if __name__ == '__main__':
	process()