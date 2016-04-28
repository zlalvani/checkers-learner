import numpy as np
import copy as cp
from move import Move
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, \
	WIN, CONTINUE, LOSE, TIE

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
		self.__moves = {RED : None, BLACK : None}
		self.__pieces = {RED : None, BLACK : None}

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
				return any(move == bd[1] for bd in self.__moves[color])
			else:
				self.getMoveList(color)
				return self.verifyMove(color, move = move)
		else:
			return False

	def getMoveList(self, color):
		if self.__moves[color] is not None:
			return cp.deepcopy(self.__moves[color])
		else:
			self.__moves[color] = self.__checkForMoves(color)
			return self.getMoveList(color)

	def getPieces(self, color):
		#look into named tuples for pieces
		if self.__pieces[color] is not None:
			return cp.deepcopy(self.__pieces[color])
		else:
			self.__pieces[color] = self.__storePieceLocations(color)
			return self.getPieces(color)

	def checkGameStatus(self, color):
		assert(not (self.getMoveList(color) == 0 and self.getMoveList(-color) == 0))
		if len(self.getMoveList(color)) == 0:
			return LOSE
		if len(self.getMoveList(-color)) == 0:
			return WIN
		return CONTINUE

	def getInverse(self):
		return Board(new_array = np.array([-p for p in (self.getArray().tolist())[::-1]]))

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
				if piece not in [RED, BLACK, RKING, BKING, EMPTY]:
					print piece
				line += piece_dic[piece] + ' '
			line += '.'
			print line
		print hline

	def applyMove(self, new_move):
		move_board = Board(self)
		piece = new_move.piece
		multiple = new_move.multiple
		row = piece[0]
		col = piece[1]
		color = new_move.color

		assert(multiple in [1, 2])
		assert(row in range(8) and col in range(8))

		# A move with a king that only goes forward should
		# also be possible with a regular piece.

		if np.sign(move_board.__grid[row][col]) != color:
			return None

		king = (move_board.__grid[row][col] == RKING or move_board.__grid[row][col] == BKING)

		dirs = [FORWARD_LEFT, FORWARD_RIGHT, int(king) * BACKWARD_LEFT, int(king) * BACKWARD_RIGHT]
		dirs = [d for d in dirs if d != 0]

		for d in new_move.getChain():
			if d not in dirs:
				return None
			res1 = move_board.__checkDirection(color, row, col, d, 1)
			res2 = move_board.__checkDirection(color, row, col, d, 2)

			if multiple == 1:
				if res1 is not None and res1[0] == EMPTY:
					val = move_board.__grid[row][col]
					move_board.__grid[row][col] = EMPTY
					move_board.__grid[res1[1]][res1[2]] = val
					if not king:
						if (res1[1] == 0 and color == RED) or (res1[1] == 7 and color == BLACK):
							move_board.__grid[res1[1]][res1[2]] *= 2
							if self.__grid[row][col] not in [RED, BLACK]:
								print self.__grid[row][col]
								raise Exception()
						#if the move is valid, it should end after a piece is kinged, but we should confirm
					row = res1[1]
					col = res1[2]
				else: return None

			elif multiple == 2:
				if res1 is not None and res2 is not None \
				and np.sign(res1[0]) == -color \
				and res2[0] == EMPTY:
					move_board = Board(self)
					
					move_board.__grid[res2[1]][res2[2]] = move_board.__grid[row][col]
					move_board.__grid[res1[1]][res1[2]] = EMPTY
					move_board.__grid[row][col] = EMPTY
					
					if not king: 
						if (res2[1] == 0 and color == RED) or (res2[1] == 7 and color == BLACK):
							move_board.__grid[res2[1]][res2[2]] *= 2
							if self.__grid[row][col] not in [RED, BLACK]:
								print self.__grid[row][col]
								raise Exception()
							#if the move is valid, it should end after a piece is kinged, but we should confirm

					row = res2[1]
					col = res2[2]

				else:
					# self.printBoard()
					# new_move.printMove()
					# raise Exception() 
					return None

		return move_board

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
				if np.sign(int(self.__grid[row][col])) == color:
					jumps_list += self.__getPieceJumps(color, row, col)
					moves_list += self.__getPieceMoves(color, row, col)
		return (jumps_list if len(jumps_list) > 0 else moves_list)

	def __getPieceJumps(self, color, row, col, piece_jumps = None, depth_flag = False, move = None, new_king = False):

		#http://effbot.org/zone/default-values.htm
		if piece_jumps is None:
			piece_jumps = []

		king = (self.__grid[row][col] == RKING or self.__grid[row][col] == BKING)

		dirs = [FORWARD_LEFT, FORWARD_RIGHT, int(king) * BACKWARD_LEFT, int(king) * BACKWARD_RIGHT]
		dirs = [d for d in dirs if d != 0]
		move_flag = False
		for d in dirs:
			res1 = self.__checkDirection(color, row, col, d, 1)
			res2 = self.__checkDirection(color, row, col, d, 2)
			if res1 is not None and res2 is not None \
			and np.sign(res1[0]) == -color \
			and res2[0] == EMPTY \
			and new_king == False:
				move_board = Board(self)
				if move is None:
					move = Move((row, col, color), d, multiple = 2)
					new_move = move
				else:
					new_move = cp.deepcopy(move)
					new_move.add(d)

				#check for king here: 

				move_board.__grid[res2[1]][res2[2]] = move_board.__grid[row][col]
				move_board.__grid[res1[1]][res1[2]] = EMPTY
				move_board.__grid[row][col] = EMPTY
				king_flag = False
				if not king: 
					if (res2[1] == 0 and color == RED) or (res2[1] == 7 and color == BLACK):
						move_board.__grid[res2[1]][res2[2]] *= 2
						if self.__grid[row][col] not in [RED, BLACK]:
							print self.__grid[row][col]
							raise Exception()
						king_flag = True
				# else:
				# 	king_flag = False

				move_flag = True
				move_board.__getPieceJumps(color, res2[1], res2[2], piece_jumps, depth_flag = True, move = new_move, new_king = king_flag)

		if not move_flag and depth_flag:
			piece_jumps.append((Board(self), cp.deepcopy(move)))
			return

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
				if not king: 
					if (result[1] == 0 and color == RED) or (result[1] == 7 and color == BLACK):
						move_board.__grid[result[1]][result[2]] *= 2
						if self.__grid[row][col] not in [RED, BLACK]:
							print self.__grid[row][col]
							raise Exception()

				piece_moves.append((move_board, new_move))


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
