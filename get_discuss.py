from xml.dom.minidom import parseString
import json
import time

from dicttoxml import dicttoxml

from func.tg_user import search, get_entity


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

def get_styled(req):
	all = []
	
	for i in req:
		entity = get_entity(i.chat_id)

		req = {
			'source': {
				'dialogs': i.chat_id,
				'id': entity.id,
			},
			'id': i.id,

			'cont': i.message,

			'time': time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(i.date.timestamp())),
			'views': i.views,
		}

		if i.is_private:
			req['source']['name'] = entity.first_name
			if entity.last_name:
				req['source']['name'] += ' ' + entity.last_name
		
		else:
			req['source']['name'] = entity.title

		all.append(req)

		


	return all

def search_json(req, count):
	res = search(req, count)
	return get_json(res, req)

def search_xml(req, count):
	res = search(req, count)
	return get_xml(res, req)

def search_styled(req, count):
	res = search(req, count)
	return get_styled(res)


if __name__ == '__main__':
	inp = 'Керчь'

	req = search(inp, 5)

	res = get_xml(req, inp)
	with open('data/res.xml', 'w') as file:
		print(res, file=file)

	res = get_json(req, inp)
	with open('data/res.json', 'w') as file:
		print(res, file=file)

	res = get_styled(req)
	print(res)