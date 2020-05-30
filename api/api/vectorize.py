import os
import sys
import csv
import json
import random

import re
# from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer
import nltk

from mongodb import db


CUT_FREQUENCY = True
CUT_POS = True
CUT_STOP_WORDS = True
SPLITTING = False
MIN_SIZE = 2 # 50
MAX_SIZE = 300
ALLOWED_POS = ('noun', 'adjf', 'adjs', 'comp', 'verb', 'infn', 'prtf', 'prts', 'grnd')
STOP_WORDS = {'июль', 'февраль', 'news', 'run', 'или', 'true', 'window', 'подписаться', 'utm', 'пока', 'третье', 'для', 'templates', 'easily', 'multiplayer', 'сайт', 'make', 'чо', 'tv', 'the', 'аж', 'на', 'think', 'settings', 'после', 'relatedvideosheight', 'ещё', 'from', 'see', 'subject', 'org', 'хотеть', 'либо', 'сейчас', 'чем', 'seem', 'с', 'try', 'апрель', 'also', 'would', 'easy', 'дабла', 'где', 'можно', 'io', 'go', 'wy', 'до', 'ты', 'подпишись', 'стать', 'could', 'com', 'май', 'самыи', 'д', 'may', 'декабрь', 'очень', 'lack', 'сеичас', 'от', 'он', 'ru', 'такои', 'о', 'right', 'к', 'enabled', 'канал', 're', 'лента', 'июнь', 'eagleplayer', 'этом', 'р', 'www', 'который', 'ять', 'rather', 'рассказать', 'об', 'relatedVideosHeight', 'весь', 'свой', 'объясняем', 'чтомнесэтыи', 'январь', 'у', 'лишь', 'но', 'россия', 'ноябрь', 'я', 'это', 'youtube', 'not', 'scroll', 'use', 'know', 'http', 'v', 'в', 'line', 'many', 'второе', 'фотограффия', 'было', 'say', 'не', 'август', 'е', 'быть', 'также', 'need', 'false', 'наш', 'get', 'some', 'т', 'октябрь', 'год', 'even', 'объяснять', 'good', 'come', 'do', 'edu', 'как', 'сообщать', 'саит', 'чуть', 'lot', 'ру', 'посмотреть', 'и', 'components', '_', 'если', 'й', 'а', 'ramblercommentscounter', 'любой', 'этот', 'take', 'они', 'месяц', 'часто', 'что', 'thank', 'мы', 'почти', 'фото', 'want', 'life', 'сентябрь', 'мочь', 'instagram', 'таки', 'за', 'минута', 'be', 'март', 'thebell', 'done', 'из', 'х', 'вы', 'nice', 'https'}


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

def doc2set(compilation, cut_speech):
	docs = [el for el in db['messages'].find({'discussion': compilation}, {'cont': True})]
	docs_ind = [el['_id'] for el in docs]
	docs = [el['cont'].strip() for el in docs]

	print('!START!', len(docs))

	for i in range(len(docs)):
		print(docs[i])

		processed = str2set(docs[i])
		if MIN_SIZE <= len(processed) <= MAX_SIZE:
			docs[i] = processed
		else:
			docs[i] = []

	return docs, docs_ind

def word_bag(data_list, frequency=CUT_FREQUENCY, stop=CUT_STOP_WORDS):
	corpus = set()
	data = [set(i) for i in data_list]

	for i in data:
		corpus = corpus | i

	# Частотное отсеивание

	if frequency:
		freq = {word: 0 for word in corpus}

		for el in data:
			for word in el:
				freq[word] += 1

		# ? Сделать по нормальному распределению

		counts = freq.values()
		freq_max = max(counts)

		# print(freq)

		for i in freq:
			if freq[i] <= 2: # freq[i] > freq_max * 0.95 or freq[i] < freq_max * 0.2:
				corpus.remove(i)

	# Стоп-слова

	if stop:
		stopwords = set(nltk.corpus.stopwords.words('russian'))
		stopwords = stopwords | STOP_WORDS

		corpus = corpus - stopwords

	#

	freq_corpus = {i: freq[i] for i in corpus}

	return tuple(corpus), freq_corpus

def set2vector(data, corpus):
	return [int(j in data) for j in corpus]

def set2obj(data, corpus):
	objs = []

	for i in range(len(data)):
		objs.append(set2vector(data[i], corpus))

	return objs

def set_proc(texts, corpus):
	texts_new = texts + []

	corpus = set(corpus)

	for i in range(len(texts_new)):
		text_words = set(texts_new[i]) & corpus

		if MIN_SIZE <= len(text_words) <= MAX_SIZE:
			texts_new[i] = list(text_words)
		else:
			texts_new[i] = []

	return texts_new

def vectorize(compilation, frequency=CUT_FREQUENCY, cut_speech=CUT_POS):
	texts, inds = doc2set(compilation, cut_speech=cut_speech)
	corpus, freq = word_bag(texts, frequency)
	sets = set_proc(texts, corpus)
	# vectors = set2obj(texts, corpus)

	print('!MIDDLE!', len(texts))
	print('!FINISH!', len(sets))

	return texts, sets, inds, corpus, freq


if __name__ == '__main__':
	compilation = 7
	texts, sets, inds, corpus, freq = vectorize(compilation)

	print('\nDataset: {}\nCorpus: {}\n'.format(len(sets), len(corpus)))