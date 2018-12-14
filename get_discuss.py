from user import search

from dicttoxml import dicttoxml

import chardet
from xml.dom.minidom import parseString


def format(req='Керчь', count=5):
	all = []

	for i in search(req, count).messages:
		all.append({
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
		})

	return all

def toxml(obj):
	res = dicttoxml(obj, attr_type=False).decode('utf-8')
	return parseString(res).toprettyxml()

if __name__ == '__main__':
	res = toxml(format())
	with open('res.xml', 'w') as file:
		print(res, file=file)