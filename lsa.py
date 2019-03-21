import csv

import numpy as np
import matplotlib.pyplot as plt


COMPILATION = 'polytics'


def read(name, sign=','):
	with open(name+'.csv', 'r') as file:
		return [i for i in csv.reader(file, delimiter=sign, quotechar=' ')]


vectors = np.array(read('data/history/{}/vectors'.format(COMPILATION)), dtype='float')
matrixs = np.linalg.svd(vectors)

print(matrixs)

plt.plot(matrixs[0][0, :], matrixs[0][1, :], 'o')
plt.show()