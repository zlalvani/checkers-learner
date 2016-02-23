import numpy as np

class Board(object):
	'''A class to represent board states, built around 2D numpy.array'''
	grid = np.array([])
	def __init__(self, board = None):
		if board: 
			self.grid = board.grid
		else:
			self.__newBoard()


	def verifyMove():
		pass


	def getMoveList(self, color):
		jumps_list = __checkForJumps(color)
		if len(jumps_list):
			return jumps_list
		else:
			return __checkForMoves(color)

	def __checkForJumps(self, color):
		jumps_list = []
		for row in range(8):
			for col in range(8):
				if np.sign(self.grid[row][col]) == color:
					result = __getPieceJumps(row, col)
					if len(result):
						jumps_list += result
		pass
	def __getPieceJumps(self, color, row, col):

		king = (abs(self.grid[row][col]) == 2)

		piece_jumps = []

		next_row = row - (color if (row - color >= 0 and row - color < 8) else 0)
		next_col = col + (1 if row + 1 < 8 else 0)
		if self.grid[next_row][next_col] == -color:
			pass

		return piece_jumps

		#recursively check for jumps to make a chain

		pass

	def __checkForMoves(self, color):
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
							[ 0,-1, 0,-1, 0,-1, 0,-1],
							[-1, 0,-1, 0,-1, 0,-1, 0],
							[ 0,-1, 0,-1, 0,-1, 0,-1],
							[ 0, 0, 0, 0, 0, 0, 0, 0],
							[ 0, 0, 0, 0, 0, 0, 0, 0],
							[ 1, 0, 1, 0, 1, 0, 1, 0],
							[ 0, 1, 0, 1, 0, 1, 0, 1],
							[ 1, 0, 1, 0, 1, 0, 1, 0],
							])



#Note: eventually use pickle to store in mongo