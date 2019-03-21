import csv

import gensim
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def read(name, sign=','):
	with open(name+'.csv', 'r') as file:
		return [i for i in csv.reader(file, delimiter=sign, quotechar=' ')]


sentences = read('data/history/polytics/texts')

model = gensim.models.Word2Vec(sentences, size=150, window=5, min_count=5, workers=4)
model.save('data/history/polytics/model.model')


def tsne_plot(model):
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    plt.figure(figsize=(16, 16)) 
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    
    plt.savefig('re.png', format='png', dpi=150)
    plt.show()

tsne_plot(model)