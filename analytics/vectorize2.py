import os
import sys
import csv
import json
import random

import re
# from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer
import nltk


CUT_FREQUENCY = False
CUT_POS = True
CUT_STOP_WORDS = True
CUT_SHORT = False
SPLITTING = False
SET_SIZE = 300
TEST_RATE = 0 # 0.2
ALLOWED_POS = ('noun', 'adjf', 'adjs', 'comp', 'verb', 'infn', 'prtf', 'prts', 'grnd')
STOP_WORDS = {'февраль', 'вы', 'об', 'р', 'т', 'www', 'чтомнесэтыи', 'use', 'фотограффия', 'такои', 'components', 'это', 'https', 'true', 'seem', 'д', 'take', 'рассказать', 'было', 'очень', 'may', 'апрель', 'easily', 'com', 'весь', 'ять', 'канал', 'за', 'фото', 'enabled', 'после', 'news', 'и', 'would', 'templates', 'tv', 'объясняем', 'ноябрь', 'х', 'lack', 'мочь', 'сентябрь', 'посмотреть', 'make', 'false', 'relatedVideosHeight', 'need', 'get', 'try', 'scroll', 'the', 'россия', 'октябрь', 'many', 'relatedvideosheight', 'любой', 'а', 'easy', 'good', 'часто', 'стать', 'также', 'multiplayer', 'март', 'ramblercommentscounter', 'е', 'который', 'org', 'lot', 'nice', 'объяснять', 'хотеть', 're', 'go', 'know', 'минута', 'январь', 'edu', 'youtube', 'лента', 'line', 'самыи', 'если', 'come', 'also', 'они', 'дабла', 'мы', 'window', 'instagram', 'декабрь', 'could', 'do', 'wy', 'этом', 'thank', 'й', 'v', 'сайт', 'thebell', 'я', 'http', 'в', 'год', 'месяц', 'чем', 'о', 'ру', 'life', 'но', 'аж', 'подписаться', '_', 'done', 'ещё', 'пока', 'ru', 'settings', 'think', 'можно', 'почти', 'на', 'у', 'right', 'сообщать', 'лишь', 'utm', 'be', 'сейчас', 'подпишись', 'not', 'some', 'сеичас', 'саит', 'либо', 'август', 'май', 'want', 'наш', 'run', 'see', 'rather', 'свой', 'июнь', 'io', 'even', 'say', 'eagleplayer', 'июль', 'subject', 'from', 'третье', 'второе', 'для', 'не', 'и', 'за', 'как', 'очень', 'с', 'на', 'я', 'у', 'для', 'где', 'что', 'ты', 'в', 'до', 'он', 'от', 'чуть', 'быть', 'к', 'вы', 'из', 'чо', 'таки', 'этот', 'или'}


# def lemmatize(text):
# 	processed = Mystem().analyze(text)
# 	lemma = lambda word: word['analysis'][0]['lex'].lower().strip()
# 	return set(lemma(word) for word in processed if 'analysis' in word)

def lemmatize(text, cut_speech=CUT_POS):
	m = MorphAnalyzer()

	def lemma(word):
		word = m.parse(word)[0]
		
		# Отсеивание частей речи
		speech = word.tag.POS

		if not cut_speech or (speech and speech.lower() in ALLOWED_POS):
			return word.normal_form

	return set(lemma(word) for word in text.split()) - {None}

def str2set(text, cut_speech=CUT_POS):
	text = re.sub(r'[^a-zA-Zа-яА-Я]', ' ', text)
	return lemmatize(text, cut_speech)

def doc2set(compilation, size=SET_SIZE, splitting=SPLITTING, cut_speech=CUT_POS, test_rate=TEST_RATE):
	url = 'data/{}/'.format(compilation)

	# Уравнять количество текстов из каждого документов

	max_count = min([len(file) for file in os.listdir(url) if '.json' in file])

	#

	files = [file for file in os.listdir(url) if '.json' in file]
	print(files)
	cont = []

	for name in files:
		category = name.split('.')[0]
		i = 0

		with open(url + name, 'r') as file:
			for string in file: # enumerate
				# Уравнять количество текстов из каждого документов

				if i >= max_count:
					break

				#

				processed = list(str2set(json.loads(string)['cont'], cut_speech)) # name

				while True:
					el_size = len(processed)

					# Если слишком неинформативный

					if CUT_SHORT and el_size < 50:
						break
					
					# Уравнивание документов (разбиение на равные куски)

					if el_size > size:
						if splitting:
							current = processed[:size]
							processed = processed[size:]
						else:
							break

					else:
						current = processed[:]
						processed = {}
					
					#

					req = {
						'category': category,
						'cont': set(current),
					}

					cont.append(req)
					i += 1

	random.shuffle(cont)
	categories = list(set([i['category'] for i in cont]))

	# Тестовая выборка

	count = int(len(cont) * test_rate)
	test = cont[:count]
	train = cont[count:]

	#

	return train, test, categories

def word_bag(data, frequency=CUT_FREQUENCY, stop=CUT_STOP_WORDS):
	corpus = set()

	for i in data:
		corpus = corpus | i['cont']

	# Частотное отсеивание

	if frequency:
		freq = {word: 0 for word in corpus}

		for el in data:
			for word in el['cont']:
				freq[word] += 1

		# ? Сделать по нормальному распределению

		counts = freq.values()
		freq_max = max(counts)

		print(freq)

		for i in freq:
			if freq[i] <= 3: # freq[i] > freq_max * 0.95 or freq[i] < freq_max * 0.2:
				corpus.remove(i)

	# Стоп-слова

	if stop:
		stopwords = set(nltk.corpus.stopwords.words('russian'))
		stopwords = stopwords | STOP_WORDS

		corpus = corpus - stopwords

	#

	return tuple(corpus)

def set2vector(data, corpus):
	return [int(j in data) for j in corpus]

def set2obj(data, corpus, categories):
	for i in range(len(data)):
		category_vec = [int(j == data[i]['category']) for j in categories]
		word_vec = set2vector(data[i]['cont'], corpus)

		data[i] = category_vec + word_vec

	return data

def obj2csv(vectors, corpus, categories):
	return [categories + ['"{}"'.format(el) for el in corpus]] + vectors

def vectorize(compilation, frequency=CUT_FREQUENCY, cut_speech=CUT_POS):
	train, test, categories = doc2set(compilation, cut_speech=cut_speech)
	corpus = word_bag(train, frequency)

	vectors_train = set2obj(train, corpus, categories)
	vectors_test = set2obj(test, corpus, categories)

	csv_train = obj2csv(vectors_train, corpus, categories)
	csv_test = obj2csv(vectors_test, corpus, categories)

	return csv_train, csv_test, corpus, categories

def write(data, compilation, name, sign=','):
	name = 'data/{}/{}.csv'.format(compilation, name)

	# Для записи матриц
	if type(data) not in (list, tuple) or type(data[0]) not in (list, tuple):
		data = [data]

	with open(name, 'w') as file:
		for i in data:
			csv.writer(file, delimiter=sign, quotechar=' ', quoting=csv.QUOTE_MINIMAL).writerow(i)


if __name__ == '__main__':
	name = sys.argv[1]
	frequency = (False if sys.argv[2] == 'x' else True) if len(sys.argv) >= 3 else CUT_FREQUENCY
	cut_speech = (False if sys.argv[3] == 'x' else True) if len(sys.argv) >= 4 else CUT_POS

	train, test, corpus, categories = vectorize(name, frequency, cut_speech)

	write(train, name, 'train')
	write(test, name, 'test')
	write(corpus, name, 'corpus')
	write(categories, name, 'categories')

	# Отображение

	ds_train = len(train) - 1
	ds_test = len(test) - 1

	print('\nDataset: {} ({} + {})\nCorpus: {}\nCategories: {}\n{}\n'.format(ds_train+ds_test, ds_train, ds_test, len(corpus), len(categories), ' | '.join(categories)))