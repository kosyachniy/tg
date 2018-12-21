#!flask/bin/python
from flask import Flask, render_template

from func.tg_user import get_me


app = Flask(__name__)


@app.route('/')
@app.route('/<search>')
@app.route('/<search>/')
def index(search=''):
	return render_template('index.html',
		user=get_me(),
	)


if __name__ == '__main__':
	app.run(debug=True, port=8000)