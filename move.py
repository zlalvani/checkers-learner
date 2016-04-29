import numpy as np
import copy as cp
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT


class Move(object):
	'''A class to represent a Move, i.e. a chain of piece coordinate updates'''
	def __init__(self, piece, direction = None, move_positions = None, multiple = 1):
		assert(direction in [FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, None])
		# assert(multiple in [1, 2])
		# assert(piece[2] in [RED, BLACK])
		self._chain = []
		self.multiple = multiple
		self.piece = piece #tuples are immutable so we shouldn't have to copy
		self.color = piece[2]
		self.valid = True
		if self.color not in [RED, BLACK]:
			self.valid = False
			return
		if self.multiple not in [1, 2]:
			self.valid = False
			return
		if direction is not None:
			self.add(direction)
		elif move_positions is not None:

			last_row = self.piece[0]
			last_col = self.piece[1]

			for pos in move_positions:
				new_row = pos[1]
				new_col = pos[0]
				if abs(last_col - new_col) != multiple \
				or abs(last_row - new_row) != multiple:
					self.valid = False
					return
				else:
					self.add(getDirection(last_row, last_col, new_row, new_col, self.color))
				last_col = new_col
				last_row = new_row

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
			BLACK : 'BLACK'
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


def getDirection(last_row, last_col, new_row, new_col, color):
	dir_tup = (np.sign(new_row - last_row), np.sign(new_col - last_col))

	if (dir_tup == (-1, -1) and color == RED) or (dir_tup == (1, 1) and color == BLACK):
		return FORWARD_LEFT
	elif (dir_tup == (-1, 1) and color == RED) or (dir_tup == (1, -1) and color == BLACK):
		return FORWARD_RIGHT
	elif (dir_tup == (1, -1) and color == RED) or (dir_tup == (-1, 1) and color == BLACK):
		return BACKWARD_LEFT
	elif (dir_tup == (1, 1) and color == RED) or (dir_tup == (-1, -1) and color == BLACK):
		return BACKWARD_RIGHT
