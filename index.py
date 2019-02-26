#!flask/bin/python
from flask import Flask, render_template

from func.tg_user import get_me, search
# from get_discuss import search_json


app = Flask(__name__)


@app.route('/')
@app.route('/<text>')
@app.route('/<text>/')
def index(text='Керчь'):
	user = get_me()
	res = search(text, 5).messages

	return render_template('index.html',
		user=user,
		cont=res,
	)


context = ('', '')

app.run(
	host='0.0.0.0',
	port=80,
	debug=True,
	threaded=True,
	# ssl_context=context,
)