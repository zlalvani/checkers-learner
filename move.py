import numpy as np
import copy as cp
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT


class Move(object):
	'''A class to represent a Move, i.e. a chain of piece coordinate updates'''
	def __init__(self, piece, direction, multiple = 1):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT])
		assert(multiple in [1, 2])
		assert(piece[2] in [RED, BLACK])
		self.__chain = []
		self.__multiple = multiple
		self.__piece = piece
		self.__color = piece[2]
		self.add(direction)

	def __eq__(self, other):
		#doesn't handle opposite color but same move case
		return cmp(self.__chain, other.__chain) == 0 and cmp(self.__piece, other.__piece) == 0

	def add(self, direction):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT])
		self.__chain.append(direction)

	def clone(self):
		new_move = Move(self.__color, self.__piece, self.__direction, self.__multiple)
		new_move.__chain = cp.deepcopy(self.__chain)
		return new_move

