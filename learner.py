import numpy as np
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT

class Learner(object):
	'''
	A class that instantiates the feature space for an individual AI, 
	chooses moves, and performs learning
	'''
	def __init__(self, points = []):
		for state, weights in points:
			continue

#http://scikit-learn.org/stable/modules/neighbors.html#classification