from user import search

from dicttoxml import dicttoxml

from xml.dom.minidom import parseString
import json


def toxml(obj):
	res = dicttoxml(obj, attr_type=False).decode('utf-8')
	return parseString(res).toprettyxml()

def get_xml(req):
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

			'Keyword': req,

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

def get_json(req):
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
			'keyword': req,

			'time': i.date.timestamp(),

			'reactions': {
				'views': {
					'count': i.views,
				},
			},
		}

		all.append(el)

	return json.dumps(all, ensure_ascii=False, indent='\t')


if __name__ == '__main__':
	req = search('Керчь', 5).messages

	res = get_xml(req)
	with open('res.xml', 'w') as file:
		print(res, file=file)

	res = get_json(req)
	with open('res.json', 'w') as file:
		print(res, file=file)