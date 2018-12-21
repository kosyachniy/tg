from func.tg_user import search

from dicttoxml import dicttoxml

from xml.dom.minidom import parseString
import json


def toxml(obj):
	res = dicttoxml(obj, attr_type=False).decode('utf-8')
	return parseString(res).toprettyxml()

def get_xml(req, inp):
	all = []

	for i in req:
		el = {
			'ID': i.id,

			# 'Header': '',
			'Body': i.message,

			# 'Username': '',
			'Userlink': i.to_id.channel_id,

			# 'Hashtags': [],

			'Date': i.date.timestamp(),

			'Keyword': inp,

			'Details': {
				'Emotions': {
					'Views': i.views,
					# 'Likes': 0,
					# 'Dislikes': 0,
				},
			},
		}

		all.append(el)

	return toxml(all)

def get_json(req, inp):
	all = []

	for i in req:
		el = {
			'id': i.id,

			# 'head': ,
			'body': i.message,

			# 'author': {},

			'source': {
				'link': i.to_id.channel_id,
			},

			# 'hashtags': ,
			'keyword': inp,

			'time': i.date.timestamp(),

			'reactions': {
				'views': {
					'count': i.views,
				},
			},
		}

		all.append(el)

	return json.dumps(all, ensure_ascii=False, indent='\t')

def search_json(req):
	res = search(req, 5).messages
	return get_json(res, req)


if __name__ == '__main__':
	inp = 'Керчь'

	req = search(inp, 5).messages

	res = get_xml(req, inp)
	with open('res.xml', 'w') as file:
		print(res, file=file)

	res = get_json(req, inp)
	with open('res.json', 'w') as file:
		print(res, file=file)