import random
import numpy as np
from board import Board
from sklearn.neighbors import BallTree
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, \
	AI_COLOR, THRESHOLD, PLAYER_COLOR

class Learner(object):
	'''
	A class that instantiates the feature space for an individual AI,
	chooses moves, and performs learning
	'''
	def __init__(self, data_points = [], current_game = [], threshold = THRESHOLD):
		self.state_list = []
		self.weights_list = []
		for state, weights in data_points:
			assert(len(state) == 32)
			self.state_list.append(state)
			self.weights_list.append(weights)

		self.threshold = threshold

		#self.__featureTransform()
		self.X = np.array(self.state_list)

		assert(self.X.shape == (len(data_points), 32) or len(data_points) == 0)
		#Think about different distance metrics. Manhattan or minkowski?
		if len(data_points) > 0:
			self.__tree = BallTree(self.X, metric='manhattan')

	def getNextMove(self, current_board):

		nn_move = self.__getNearestNeighbors(current_board)
		if nn_move is not None:
			return nn_move
		else:
			return self.__getMinimax(current_board)

	def __getMinimax(self, current_board):
		(bestBoard, bestVal) = minMax2(current_board, 6)
		print("bestVal", bestVal)
		bestBoard[0].printBoard()
		return bestBoard

	def __getNearestNeighbors(self, current_board):
		#dist, ind = self.__tree.query(current_board.getArray(), k=3)
		if (len(self.weights_list) == 0):
			return None
		ind = self.__tree.query_radius(current_board.getArray(), r = self.threshold).tolist()

		#cur_moves = current_board.getMoveList(AI_COLOR)
		moves = []
		weights = []
		for i in ind:
			_board = Board(new_array = self.state_list[i])
			assert(len(_board.getMoveList(AI_COLOR)) == len(self.weights_list[i]))
			for j, (board, move) in enumerate(_board.getMoveList(AI_COLOR)):
				if current_board.verifyMove(AI_COLOR, move = move):
					moves += move
					weights += self.weights_list[i][j]
		if len(moves) == 0:
			return None
		else:
			assert(len(moves) == len(weights))
			return np.random.choice(moves, 1, weights)
		#neighbor_moves = [move for move in neighbor_moves if move in cur_moves]


	def __featureTransform(self):
		#replace weights with a Gaussian at some point
		#or come up with a better feature transform
		weights = [1, 2, 3, 4, 4, 3, 2, 1]
		transformed_list = []
		for state in self.state_list:
			assert(len(state) == 32)
			new_state = []
			for i in range(32):
				new_state.append(state[i] * weights[i / 4])
			transformed_list.append(new_state)

		self.X = np.array(transformed_list)




# -----------------------------------------------------

def minMax2(board, maxDepth):
    bestBoard = None
    currentDepth = maxDepth
    while not bestBoard and currentDepth > 0:
        currentDepth -= 1
        (bestBoard, bestVal) = maxMove2(board, currentDepth)
    return (bestBoard, bestVal)

def maxMove2(maxBoard, currentDepth):
    """
        Calculates the best move for RED player (computer) (seeks a board with INF value)
    """
    return maxMinBoard(maxBoard, currentDepth-1, float('-inf'))


def minMove2(minBoard, currentDepth):
    """
        Calculates the best move from the perspective of BLACK player (seeks board with -INF value)
    """
    return maxMinBoard(minBoard, currentDepth-1, float('inf'))

def maxMinBoard(board, currentDepth, bestMove):
    """
        Does the actual work of calculating the best move
    """
    # Check if we are at an end node
    if currentDepth <= 0:
		return (np.sum(board.getArray()), 1)

    # So we are not at an end node, now we need to do minmax
    # Set up values for minmax
    best_move_value = bestMove
    best_board = None

    # MaxNode
    if bestMove == float('-inf'):
        # Create the iterator for the Moves
        board_moves = board.getMoveList(AI_COLOR)
        for board_move in board_moves:
            board_move[0].printBoard()
            value = minMove2(board_move[0], currentDepth-1)[1]
            if value > best_move_value:
                best_move_value = value
                best_board = board_move

    # MinNode
    elif bestMove == float('inf'):
        board_moves = board.getMoveList(PLAYER_COLOR)
        for board_move in board_moves:
            value = maxMove2(board_move[0], currentDepth-1)[1]
            # Take the smallest value we can
            if value < best_move_value:
                best_move_value = value
                best_board = board_move

	best_board[0].printBoard()
    # Things appear to be fine, we should have a board with a good value to move to
    return (best_board, best_move_value)




#http://scikit-learn.org/stable/modules/neighbors.html#classification
#http://www.sciencedirect.com/science/article/pii/S0925231210003875
