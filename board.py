import numpy as np
from globalconsts import RED, BLACK, FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT

class Board(object):
	'''A class to represent board states, built around 2D numpy.array'''
	moves = {RED : [], BLACK : []}
	def __init__(self, board = None):
		if board: 
			self.grid = board.grid
		else:
			self.__newBoard()
			

	def verifyMove(self, next_board):
		pass


	def getMoveList(self, color):
		move_list = __checkForMoves(color)
		self.moves[color] = move_list
		return move_list

	def printBoard(self):
		pass

	def __checkForMoves(self, color):
		jumps_list = []
		moves_list = []
		for row in range(8):
			for col in range(8):
				if np.sign(self.grid[row][col]) == color:
					jumps_list += __getPieceJumps(color, row, col)
					moves_list += __getPieceMoves(color, row, col)
		return (jumps_list if len(jumps_list) else moves_list)

	def __getPieceJumps(self, color, row, col, piece_jumps = []):

		king = (self.grid[row][col] == RKING or self.grid[row][col] == BKING)

		'''
		next_row = row - (color if (row - color >= 0 and row - color < 8) else 0)
		next_col = col + (1 if row + 1 < 8 else 0)
		if self.grid[next_row][next_col] == -color:
			pass
		'''
		return piece_jumps

		#recursively check for jumps to make a chain

		pass

	def __checkDirection(self, color, row, col, direction, multiple = 1):
		def __fwdLeft():
			return (row - (color*multiple), col - (color*multiple)) if row % 2 == 0 \
				else (row - (color*multiple), col)
		def __fwdRight():
			return (row + (color*multiple), col) if row % 2 == 0 \
				else (row + (color*multiple), col - (color*multiple))
		def __bwdLeft():
			return (row - (color*multiple), col + (color*multiple)) if row % 2 == 0 \
				else (row - (color*multiple), col)
		def __bwdRight():
			return (row + (color*multiple), col) if row % 2 == 0 \
				else (row + (color*multiple), col + (color*multiple))

		dir_dic = { FORWARD_LEFT : __fwdLeft,
					FORWARD_RIGHT : __fwdRight,
					BACKWARD_LEFT : __bwdLeft,
					BACKWARD_RIGHT : __bwdRight
					}
		'''
		dir_dic = { FORWARD_LEFT : (row - (color*multiple), col - (color*multiple)),
					FORWARD_RIGHT : (row + (color*multiple), col - (color*multiple)),
					BACKWARD_LEFT : (row - (color*multiple), col + (color*multiple)),
					BACKWARD_RIGHT : (row + (color*multiple), col + (color*multiple)),
					0 : (-1, -1)
					}
		'''
		result = dir_dic[direction]()
		check_row = result[0]
		check_col = result[1]

		if check_row < 0 or check_col < 0:
			return None
		else:
			return self.grid[check_row][check_col], check_row, check_col

	def __getPieceMoves(self, color, row, col):
		king = (self.grid[row][col] == RKING or self.grid[row][col] == BKING)

		dirs = [FORWARD_LEFT, FORWARD_RIGHT, int(king) * BACKWARD_LEFT, int(king) * BACKWARD_RIGHT]
		dirs = [d for d in dirs if d != 0]

		piece_moves = []

		for direction in dirs:
			result = self.__checkDirection(color, row, direction)
			if result is not None: 
				if result[0] == EMPTY:
					move_board = Board(self) #maybe problem
					val = move_board.grid[row][col]
					move_board.grid[row][col] = 0
					move_board.grid[result[1]][result[2]] = val
					piece_moves.append(move_board)


		pass

	def __newBoard(self):
		'''
		-2 - black king
		-1 - black
		 0 - empty
		 1 - red
		 2 - red king
		'''
		self.grid = np.array([
							[BLACK, BLACK, BLACK, BLACK],
							[BLACK, BLACK, BLACK, BLACK],
							[BLACK, BLACK, BLACK, BLACK],
							[EMPTY, EMPTY, EMPTY, EMPTY],
							[EMPTY, EMPTY, EMPTY, EMPTY],
							[RED,   RED,   RED,   RED],
							[RED,   RED,   RED,   RED],
							[RED,   RED,   RED,   RED]
							])
		'''
		self.grid = np.array([
							[ 0,-1, 0,-1, 0,-1, 0,-1],
							[-1, 0,-1, 0,-1, 0,-1, 0],
							[ 0,-1, 0,-1, 0,-1, 0,-1],
							[ 0, 0, 0, 0, 0, 0, 0, 0],
							[ 0, 0, 0, 0, 0, 0, 0, 0],
							[ 1, 0, 1, 0, 1, 0, 1, 0],
							[ 0, 1, 0, 1, 0, 1, 0, 1],
							[ 1, 0, 1, 0, 1, 0, 1, 0],
							])
		'''


#Threshold nearest neighbor distance to choose between it and minimax
#Note: eventually use pickle to store in mongo