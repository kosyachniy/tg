from flask import Flask, render_template, request, redirect

from func.tg_user import get_me, search
from get_discuss import get_styled
from visualisation import timeline


app = Flask(__name__)


@app.route('/')
@app.route('/<text>')
@app.route('/<text>/')
def index(text='Керчь'):
	messages = search(text, 100)
	# print(len(messages))

	return render_template('index.html',
		user=get_me(),
		cont=get_styled(messages),
		timeline = timeline(messages),

		len = len,
	)

@app.route('/sys_search', methods=['POST'])
@app.route('/sys_search/', methods=['POST'])
def sys_search():
	return redirect('/' + request.form['search'])


context = ('', '')

app.run(
	host='0.0.0.0',
	port=80,
	debug=True,
	threaded=True,
)