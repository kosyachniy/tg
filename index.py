#!flask/bin/python

import time

from flask import Flask, render_template

from func.tg_user import get_me, search, get_entity
# from get_discuss import search_json


app = Flask(__name__)


@app.route('/')
@app.route('/<text>')
@app.route('/<text>/')
def index(text='Керчь'):
	user = get_me()
	res = search(text, 100).messages
	print(res[0].stringify())

	messages = []
	for i in res:
		entity = get_entity(i.chat_id)

		messages.append({
			'source': {
				'dialogs': i.chat_id,
				'id': entity.id,
				'name': '{} {}'.format(entity.first_name, entity.last_name) if i.is_private else entity.title,
			},
			'id': i.id,
			'cont': i.message,
			'time': time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(i.date.timestamp())),
			'views': i.views,
		})

	# print(dir(res[0]), res[0].chat_id, res[0].id, res[0].to_id.to_dict())
	# print(get_entity(res[0].chat_id))

	return render_template('index.html',
		user=user,
		cont=messages,
	)


context = ('', '')

app.run(
	host='0.0.0.0',
	port=80,
	debug=True,
	threaded=True,
	# ssl_context=context,
)