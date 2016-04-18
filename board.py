import numpy as np
import copy as cp
from move import Move
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT

#http://www.learnpython.org/en/Multiple_Function_Arguments

class Board(object):
	'''A class to represent board states, built around 2D numpy.array'''
	def __init__(self, board = None, new_grid = None, new_array = None, weight = 1):
		if board is not None:
			self.__grid = board.getGrid()
		elif new_grid is not None:
			self.__grid = cp.deepcopy(new_grid)
		elif new_array is not None:
			assert(len(new_array) == 32)
			self.__newBoard()
			for i in range(32):
				if i % 8 < 4:
					self.__grid[i / 4][2 * (i % 4) + 1] = new_array[i]
				else:
					self.__grid[i / 4][2 * (i % 4)] = new_array[i]
		else:
			self.__newBoard()

		self.weight = weight #figure out a way to associate a weight with each possible move

		#RED should be AI, black should be opponent
		self.__moves = {RED : [], BLACK : []}
		self.__pieces = {RED : set([]), BLACK : set([])}

	def __eq__(self, other):
		'''
			Overload the = operator to compare each element in the board
		'''
		for i, row in enumerate(self.__grid):
			for j, element in enumerate(row):
				if(element != other.__grid[i][j]):
					return False
		return True

	def getGrid(self):
		return cp.deepcopy(self.__grid)

	def getArray(self):
		array = []
		for row in range(8):
			for col in range(8):
				if row % 2 != col % 2:
					array.append(self.__grid[row][col])
		return np.array(array)

	def verifyMove(self, color, next_board = None, move = None):
		if next_board is not None:
			if len(self.__moves[color]):
				return any(next_board == bd[0] for bd in self.__moves[color])
			else:
				self.getMoveList(color)
				return self.verifyMove(color, next_board = next_board)
		elif move is not None:
			if len(self.__moves[color]):
				return any(next_board == bd[1] for bd in self.__moves[color])
			else:
				self.getMoveList(color)
				return self.verifyMove(color, move = move)
		else:
			return False


	def getMoveList(self, color):
		if len(self.__moves[color]):
			return cp.deepcopy(self.__moves[color])
		else:
			self.__moves[color] = self.__checkForMoves(color)
			return self.getMoveList(color)

	def getPieces(self, color):
		#look into named tuples for pieces
		if len(self.__pieces[color]):
			return cp.deepcopy(self.__pieces[color])
		else:
			self.__pieces[color] = self.__storePieceLocations(color)
			return self.getPieces(color)

	def getInverse(self):
		return Board(new_array = np.array([-p for p in self.getArray().tolist()]))

	def printBoard(self):
		piece_dic = {
			RED : 'r',
			BLACK : 'b',
			RKING : 'R',
			BKING : 'B',
			EMPTY : '-'
		}

		hline = '.' * 19
		print hline
		grid = self.__grid
		for row in grid:
			line = '. '
			for piece in row:
				line += piece_dic[piece] + ' '
			line += '.'
			print line
		print hline

	def __storePieceLocations(self, color):
		locs = []
		for row in range(8):
			for col in range(8):
				if np.sign(self.__grid[row][col]) == color:
					locs.append((row, col, color))
		self.__pieces[color] = set(locs)

	def __checkForMoves(self, color):
		jumps_list = []
		moves_list = []
		for row in range(8):
			for col in range(8):
				if np.sign(self.__grid[row][col]) == color:
					jumps_list += self.__getPieceJumps(color, row, col)
					print len(jumps_list)
					moves_list += self.__getPieceMoves(color, row, col)
					#print len(moves_list)
		return (jumps_list if len(jumps_list) > 0 else moves_list)

	def __getPieceJumps(self, color, row, col, piece_jumps = [], depth_flag = False, move = None):#, jump_tree = []):

		king = (self.__grid[row][col] == RKING or self.__grid[row][col] == BKING)

		dirs = [FORWARD_LEFT, FORWARD_RIGHT, int(king) * BACKWARD_LEFT, int(king) * BACKWARD_RIGHT]
		dirs = [d for d in dirs if d != 0]
		move_flag = False
		for d in dirs:
			res1 = self.__checkDirection(color, row, col, d, 1)
			res2 = self.__checkDirection(color, row, col, d, 2)
			if res1 is not None and res2 is not None \
			and np.sign(res1[0]) == -color \
			and res2[0] == EMPTY:
				move_board = Board(self)
				if move is None:
					move = Move((row, col, color), d, multiple = 2)
				else:
					move.add(d)
					#new_move = move
				move_board.__grid[res2[1]][res2[2]] = move_board.__grid[row][col]
				move_board.__grid[res1[1]][res1[2]] = EMPTY
				move_board.__grid[row][col] = EMPTY
				#new_tree.add(move)
				move_flag = True
				move_board.__getPieceJumps(color, res2[1], res2[2], piece_jumps, depth_flag = True, move = move)
		if not move_flag and depth_flag:
			print "test"
			piece_jumps.append((Board(self), cp.deepcopy(move)))
			return
		print "jumps", len(piece_jumps)
		return piece_jumps

	def __checkDirection(self, color, row, col, direction, multiple = 1):

		def __fwdLeft():
			return (row - (color*multiple), col - (color*multiple))
		def __fwdRight():
			return (row - (color*multiple), col + (color*multiple))
		def __bwdLeft():
			return (row + (color*multiple), col - (color*multiple))
		def __bwdRight():
			return (row + (color*multiple), col + (color*multiple))

		dir_dic = {
			FORWARD_LEFT : __fwdLeft,
			FORWARD_RIGHT : __fwdRight,
			BACKWARD_LEFT : __bwdLeft,
			BACKWARD_RIGHT : __bwdRight
		}

		result = dir_dic[direction]()
		check_row = result[0]
		check_col = result[1]

		if check_row < 0 or check_row > 7 or check_col < 0 or check_col > 7:
			return None
		else:
			return self.__grid[check_row][check_col], check_row, check_col

	def __getPieceMoves(self, color, row, col):
		king = (self.__grid[row][col] == RKING or self.__grid[row][col] == BKING)

		dirs = [FORWARD_LEFT, FORWARD_RIGHT, int(king) * BACKWARD_LEFT, int(king) * BACKWARD_RIGHT]
		dirs = [d for d in dirs if d != 0]

		piece_moves = []

		for d in dirs:
			result = self.__checkDirection(color, row, col, d)
			if result is not None and result[0] == EMPTY:
				move_board = Board(self) #maybe problem
				val = move_board.__grid[row][col]
				move_board.__grid[row][col] = EMPTY
				move_board.__grid[result[1]][result[2]] = val
				new_move = Move((row, col, color), d, multiple = 1)
				piece_moves.append((move_board, new_move))


				#move_board.printBoard()

		return piece_moves

	def __newBoard(self):
		'''
		-2 - black king
		-1 - black
		 0 - empty
		 1 - red
		 2 - red king
		'''

		self.__grid = [
			[ 0,-1, 0,-1, 0,-1, 0,-1],
			[-1, 0,-1, 0,-1, 0,-1, 0],
			[ 0,-1, 0,-1, 0,-1, 0,-1],
			[ 0, 0, 0, 0, 0, 0, 0, 0],
			[ 0, 0, 0, 0, 0, 0, 0, 0],
			[ 1, 0, 1, 0, 1, 0, 1, 0],
			[ 0, 1, 0, 1, 0, 1, 0, 1],
			[ 1, 0, 1, 0, 1, 0, 1, 0],
		]


#Threshold nearest neighbor distance to choose between it and minimax
#Note: eventually use pickle to store in mongo
