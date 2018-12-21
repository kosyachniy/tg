#!flask/bin/python
from flask import Flask, render_template

# from func.tg_user import *
from get_discuss import search_json


app = Flask(__name__)


@app.route('/')
@app.route('/<search>')
@app.route('/<search>/')
def index(search=''):
	user = {'login': ''} # get_me()
	res = search_json('Керчь')

	return render_template('index.html',
		user=user,
	)


if __name__ == '__main__':
	app.run(debug=True, port=8000)