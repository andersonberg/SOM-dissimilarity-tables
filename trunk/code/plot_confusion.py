import matplotlib.pyplot as plt
import numpy as np

# Base de dados E.coli
class1x = [0, 0, 1, 1, 2, 2]
class1y = [3, 4, 3, 4, 3, 4]
size1 = np.array([15, 31, 14, 22, 26, 27]) * 20

class2x = [0, 1]
class2y = [0, 0]
size2 = np.array([20, 10]) * 20

class5x = [0, 0, 0, 1]
class5y = [0, 1, 2, 2]
size5 = np.array([20, 18, 15, 7]) * 20

class8x = [2]
class8y = [2]
size8 = np.array([11]) * 20


class6x = [1, 2, 2]
class6y = [1, 0, 1]
size6 = np.array([5, 32, 11]) * 20

#plt.plot(class1x, class1y, 'ro', class2x, class2y, 'bs', class6x, class6y, 'g^')
#plt.axis([-1,5,-1,5])
#plt.axis('scaled')

plt.scatter(class1x, class1y, size1, c='r', marker='o', faceted=False)
plt.scatter(class2x, class2y, size2, c='b', marker='s', faceted=False)
plt.scatter(class5x, class5y, size5, c='y', marker='v', faceted=False)
plt.scatter(class6x, class6y, size6, c='g', marker='^', faceted=False)
plt.scatter(class8x, class8y, size8, c='k', marker='d', faceted=False)

# Bases de dados Iris

plt.show()
