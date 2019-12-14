import csv

import numpy as np
# import matplotlib.pyplot as plt
from sklearn.decomposition import LatentDirichletAllocation as lda
from sklearn.externals import joblib


COMPILATION = 'polytics'


def read(name, sign=','):
	with open(name+'.csv', 'r') as file:
		return [i for i in csv.reader(file, delimiter=sign, quotechar=' ')]

vectors = read('data/history/{}/vectors'.format(COMPILATION))
dataset = np.array(vectors, dtype='float')

model = lda(n_components = 2) # 60, max_iter=30, n_jobs=6, learning_method='batch', verbose=1)
model.fit(dataset)

for i in model.components_:
	print(i)

model.show_topic(0, topn=10)

joblib.dump(model, 'data/history/{}/lda.txt'.format(COMPILATION))