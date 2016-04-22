import numpy as np
import copy as cp
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT


class Move(object):
	'''A class to represent a Move, i.e. a chain of piece coordinate updates'''
	def __init__(self, piece, direction = None, multiple = 1):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, None])
		assert(multiple in [1, 2])
		assert(piece[2] in [RED, BLACK])
		self.__chain = []
		self.__multiple = multiple
		self.__piece = piece
		self.__color = piece[2]
		self.add(direction)

	def __eq__(self, other):
		#doesn't handle opposite color but same move case
		if other is None:
			return False
		return cmp(self.__chain, other.__chain) == 0 and cmp(self.__piece, other.__piece) == 0

	def add(self, direction):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, None])
		self.__chain.append(direction)

	def getChain(self):
		return cp.deepcopy(self.__chain)

	def clone(self):
		new_move = Move(piece = self.__piece, multiple = self.__multiple)
		new_move.__chain = self.getChain()
		return new_move

	def printMove(self):
		piece_dic = {
			RED : 'RED',
			BLACK : 'BLACK',
			RKING : 'RKING',
			BKING : 'BKING'
		}

		dir_dic = {
			FORWARD_LEFT : "FWD_LEFT",
			FORWARD_RIGHT : "FWD_RIGHT",
			BACKWARD_LEFT : "BWD_LEFT",
			BACKWARD_RIGHT : "BWD_RIGHT"
		}

		mul_dic = {
			2 : "JUMP",
			1 : "MOVE"
		}

		print piece_dic[self.__color], mul_dic[self.__multiple], "AT:", self.__piece[0], self.__piece[1]
		print "\t" + "Direction List:"
		for d in self.__chain:
			print "\t\t" + dir_dic[d]

