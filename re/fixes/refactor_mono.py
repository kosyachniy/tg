import json
import os
import re

from pymorphy2 import MorphAnalyzer


m = MorphAnalyzer()
lemma = lambda word: m.parse(word)[0].normal_form

def to_json(cont):
	return json.dumps(cont, ensure_ascii=False, indent='\t')


text_all = ''
k = 0

for i in os.listdir('data/history/'):
	if i[-4:] == 'json':
		try:
			k += 1
			with open('data/history/{}'.format(i), 'r') as file:
				for j in file:
					text = json.loads(j)['body'].strip()
					if text:
						text_all += text + '\n'
		except:
			pass

print(k)

with open('data/history/mono.txt', 'w') as file:
	print(text_all, file=file)