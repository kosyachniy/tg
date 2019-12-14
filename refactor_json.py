import json
import os
import re

from pymorphy2 import MorphAnalyzer


m = MorphAnalyzer()
lemma = lambda word: m.parse(word)[0].normal_form

def to_json(cont):
	return json.dumps(cont, ensure_ascii=False, indent='\t')


texts = []
texts_inf = []

for i in os.listdir('data/history/'):
	if i[-4:] == 'json':
		try:
			with open('data/history/{}'.format(i), 'r') as file:
				for j in file:
					text = json.loads(j)['body'].strip()
					if text:
						texts.append(text)

						text_list = re.split(r'[^a-zA-Zа-яА-Я-]', text)
						text_list_inf = [lemma(u) for u in text_list]
						text_inf = ' '.join(text_list_inf).lower()
						texts_inf.append(text_inf)
		except:
			pass

res = to_json({'content': {'{}'.format(i): j for i, j in enumerate(texts)}})
res_inf = to_json({'content': {'{}'.format(i): j for i, j in enumerate(texts_inf)}})

with open('data/history/refactor.json', 'w') as file:
	print(res, file=file)

with open('data/history/refactor_inf.json', 'w') as file:
	print(res_inf, file=file)