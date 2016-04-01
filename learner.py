import numpy as np
from sklearn.neighbors import BallTree
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT

class Learner(object):
	'''
	A class that instantiates the feature space for an individual AI, 
	chooses moves, and performs learning
	'''
	def __init__(self, points = [], threshold = THRESHOLD):
		self.state_list = []
		self.weights_list = []
		for state, weights in points:
			assert(len(state) == 32)
			self.state_list.append(state)
			self.weights_list.append(weights)

		self.threshold = threshold
		self.__featureTransform()

		assert(self.X.shape == (len(points), 32))
		#Think about different distance metrics. Manhattan or minkowski?
		self.__tree = BallTree(X, metric='manhattan')

	def getNextMove(self, current_board):


		pass

	def __getMinimax(self, current_board):
		pass

	def __getNearestNeighbors(self, current_board):
		#dist, ind = self.__tree.query(current_board.getArray(), k=3)
		ind = self.__tree.query_radius(current_board.getArray(), r = self.threshold)

		pass

	def __featureTransform(self):
		#replace weights with a Gaussian at some point
		#or come up with a better feature transform
		weights = [1, 2, 3, 4, 4, 3, 2, 1]
		transformed_list = []
		for state in self.state_list:
			assert(len(state) == 32)
			new_state = []
			for i in range(32):
				new_state.append(state[i] * weights[i / 4])
			transformed_list.append(new_state)

		self.X = np.array(transformed_list)

#http://scikit-learn.org/stable/modules/neighbors.html#classification
#http://www.sciencedirect.com/science/article/pii/S0925231210003875