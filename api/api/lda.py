import gensim
import gensim.corpora as corpora

from mongodb import db


def lda(compilation):
	db_condition = {
		'discussion': compilation,
		'preprocessed': {'$ne': []},
	}
	data = [i for i in db['messages'].find(db_condition, {'preprocessed': True})]
	data_ready = [i['preprocessed'] for i in data]
	data_inds = [i['_id'] for i in data]

	id2word = corpora.Dictionary(data_ready)
	corpus = [id2word.doc2bow(text) for text in data_ready]

	lda_model = gensim.models.ldamodel.LdaModel(
		corpus=corpus,
		id2word=id2word,
		num_topics=5,
		random_state=100,
		update_every=1,
		chunksize=10,
		passes=10,
		alpha='symmetric',
		iterations=500,
		per_word_topics=True
	)

	topics = []
	prob = []

	for i, row_list in enumerate(lda_model[corpus]):
		row = row_list[0] if lda_model.per_word_topics else row_list
		row = sorted(row, key=lambda x: (x[1]), reverse=True)
		topic, prop = row[0]

		topics.append(topic)
		prob.append(prop)

	return lda_model, corpus, data_ready, data_inds, topics, prob


if __name__ == '__main__':
	lda_model, corpus, data_ready, data_inds, topics, prob = lda(7)

	print('-'*100)
	print()
	print(*map(lambda x: x[1], lda_model.print_topics()), sep='\n\n')
	print()
	print('-'*100)

	for i in range(len(topics)):
		print('Topic: {}	|	Probability: {}'.format(topics[i], prob[i]))