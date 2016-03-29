import numpy as np
import copy as cp
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT


class Move(object):
	'''A class to represent a Move, i.e. a chain of piece coordinate updates'''
	def __init__(self, color, piece, direction, multiple = 1):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT])
		assert(multiple in [1, 2])
		assert(color in [RED, BLACK])
		self.__chain = []
		self.__multiple = multiple
		self.__color = color
		self.__piece = piece
		self.add(direction)

	def add(self, direction):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT])
		self.__chain.append(direction)

	def clone(self):
		new_move = Move(self.__color, self.__piece, self.__direction, self.__multiple)
		new_move.__chain = cp.deepcopy(self.__chain)
		return new_move

