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
		self._chain = []
		self.multiple = multiple
		self.piece = piece #tuples are immutable so we shouldn't have to copy
		self.color = piece[2]
		self.add(direction)

	def __eq__(self, other):
		#doesn't handle opposite color but same move case
		if other is None:
			return False
		return cmp(self._chain, other._chain) == 0 and cmp(self.piece, other.piece) == 0

	def add(self, direction):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, None])
		self._chain.append(direction)

	def getChain(self):
		return cp.deepcopy(self._chain)

	def clone(self):
		new_move = Move(piece = self.piece, multiple = self.multiple)
		new_move._chain = self.getChain()
		return new_move

	def getInverse(self):
		new_piece = (7 - self.piece[0], 7 - self.piece[1], -self.color)
		new_move = Move(piece = new_piece, multiple = self.multiple)
		new_move._chain = self.getChain()
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

		print piece_dic[self.color], mul_dic[self.multiple], "AT:", self.piece[0], self.piece[1]
		print "\t" + "Direction List:"
		for d in self._chain:
			print "\t\t" + dir_dic[d]

