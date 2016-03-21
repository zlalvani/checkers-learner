import numpy as np
import copy as cp
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT

class Board(object):
	'''A class to represent board states, built around 2D numpy.array'''
	def __init__(self, board = None, new_grid = None):
		if board is not None and new_grid is None: 
			self.__grid = board.getGrid()

			#self.__grid = np.array(board.__grid)
		if board is None and new_grid is not None:
			self.__grid = cp.deepcopy(new_grid)
		else:
			self.__newBoard()

		self.moves = {RED : [], BLACK : []}
			


	def getGrid(self):
		return cp.deepcopy(self.__grid)

	def verifyMove(self, color, next_board):
		if len(self.moves[color]):
			return (next_board in self.moves[color])
		else:
			self.getMoveList(color)
			return self.verifyMove(color, next_board)


	def getMoveList(self, color):
		if not len(self.moves[color]):
			move_list = self.__checkForMoves(color)
			self.moves[color] = move_list
		else:
			move_list = self.moves[color]
		return move_list

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
		#__grid = self.__grid.tolist()
		grid = self.__grid
		for row in grid:
			line = '. '
			for piece in row:
				line += piece_dic[piece] + ' '
			line += '.'
			print line
		print hline

	def __checkForMoves(self, color):
		jumps_list = []
		moves_list = []
		for row in range(8):
			for col in range(8):
				if np.sign(self.__grid[row][col]) == color:
					jumps_list += self.__getPieceJumps(color, row, col)
					moves_list += self.__getPieceMoves(color, row, col)
		#print "# of moves:", len(moves_list)
		#print "# of jumps:", len(jumps_list)
		return (jumps_list if len(jumps_list) else moves_list)

	def __getPieceJumps(self, color, row, col, piece_jumps = [], depth_flag = False):#, jump_tree = []):

		king = (self.__grid[row][col] == RKING or self.__grid[row][col] == BKING)

		dirs = [FORWARD_LEFT, FORWARD_RIGHT, int(king) * BACKWARD_LEFT, int(king) * BACKWARD_RIGHT]
		dirs = [d for d in dirs if d != 0]
		move_flag = False
		for d in dirs:
			#new_tree = jump_tree[:]
			res1 = self.__checkDirection(color, row, col, d, 1)
			res2 = self.__checkDirection(color, row, col, d, 2)
			if res1 is not None and res2 is not None \
			and np.sign(res1[0]) is -color \
			and res2[0] is EMPTY:
				move = Board(self)
				move.__grid[row][col] = EMPTY
				move.__grid[res1[1]][res1[2]] = EMPTY
				move.__grid[res2[1]][res2[2]] = color
				#new_tree.add(move)
				move_flag = True
				move.__getPieceJumps(color, res2[1], res2[2], piece_jumps, depth_flag = True)
		if not move_flag and depth_flag:
			piece_jumps.append(Board(self))
		

		'''
		next_row = row - (color if (row - color >= 0 and row - color < 8) else 0)
		next_col = col + (1 if row + 1 < 8 else 0)
		if self.__grid[next_row][next_col] == -color:
			pass
		'''
		return piece_jumps

		#recursively check for jumps to make a chain

	def __checkDirection(self, color, row, col, direction, multiple = 1):
		#these have bugs
		'''
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
		'''
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
			if result is not None and result[0] is EMPTY: 
				move_board = Board(self) #maybe problem
				val = move_board.__grid[row][col]
				move_board.__grid[row][col] = EMPTY
				move_board.__grid[result[1]][result[2]] = val
				piece_moves.append(move_board)

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
		#use the following representation for ML:
		'''
		self.__grid = np.array([
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