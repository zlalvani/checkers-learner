import numpy as np
import copy as cp
import random
from board import Board
from sklearn.neighbors import BallTree
from globalconsts import \
    EMPTY, RED, BLACK, BKING, RKING, \
    FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, \
    AI_COLOR, THRESHOLD, PLAYER_COLOR, \
    LOSE, WIN, CONTINUE, TIE, \
    WIN_FACTOR, LOSE_FACTOR

class Learner(object):
	"""
	A class that instantiates the feature space for an individual AI,
	chooses moves, and performs learning
	"""
	def __init__(self, data_points = None, ai_history = None, threshold = THRESHOLD):
		self.state_list = []
		self.weights_list = []

		if data_points is None:
			data_points = []
		if ai_history is None:
			ai_history = []

		for state, weights in data_points:
			assert(len(state) == 32)
			self.state_list.append(state)
			self.weights_list.append(weights)

		self._threshold = threshold
		self._ai_history = cp.deepcopy(ai_history)

		#self._featureTransform()
		self.X = np.array(self.state_list)

		assert(self.X.shape == (len(data_points), 32) or len(data_points) == 0)
		#Think about different distance metrics. Manhattan or minkowski? P < 1?
		if len(data_points) > 0:
			self._tree = BallTree(self.X, metric='manhattan')
		else:
			self._tree = None

	def getNextMove(self, current_board):
		# current_board.printBoard()
		nn_move = self._getNearestNeighbors(current_board)
		if nn_move is not None:
			next_move = nn_move
		else:
			next_move = self._getMinimax(current_board)
		self._ai_history.append(next_move)
		return next_move

	def updateWeights(self, game_history, status):
		
		if status == WIN:
			factor = WIN_FACTOR
		elif status == LOSE:
			factor = LOSE_FACTOR
		elif status == TIE:
			factor = 1

		# old_board = Board()
		for _board, _move in game_history:
			assert(any(_move == mv[1] for mv in _board.getMoveList(_move.color)))

			if _move.color == AI_COLOR:
				state = _board.getArray().tolist()

				if state in self.state_list:
					i = self.state_list.index(state)
					# j = self.state_list[i].find(move)
					# print zip(*_board.getMoveList(AI_COLOR))[1]
					# print list(zip(*_board.getMoveList(AI_COLOR))[1])
					j = list(zip(*_board.getMoveList(AI_COLOR))[1]).index(_move)
					self.weights_list[i][j] *= factor

				else:
					self.state_list.append(state)
					self.weights_list.append([1] * len(_board.getMoveList(AI_COLOR)))
					# print zip(*_board.getMoveList(AI_COLOR))[1]
					j = list(zip(*_board.getMoveList(AI_COLOR))[1]).index(_move)
					self.weights_list[-1][j] *= factor

			elif _move.color == PLAYER_COLOR:
				_move = _move.getInverse()
				state = _board.getInverse().getArray().tolist()

				if state in self.state_list:
					i = self.state_list.index(state)
					# j = self.state_list[i].find(move)
					j = list(zip(*_board.getInverse().getMoveList(AI_COLOR))[1]).index(_move)
					self.weights_list[i][j] *= (1.0 / factor)

				else:
					self.state_list.append(state)
					self.weights_list.append([1] * len(_board.getInverse().getMoveList(AI_COLOR)))
					j = list(zip(*_board.getInverse().getMoveList(AI_COLOR))[1]).index(_move)
					self.weights_list[-1][j] *= (1.0 / factor)

		self.X = np.array(self.state_list)
		self._tree = BallTree(self.X, metric='manhattan')

			# old_board = board


	# def updateWeights(self, end_board, player_history, ai_history = None, status = None, ai_first = False, game_history = None):
	# 	if status is None:
	# 		status = end_board.checkGameStatus(AI_COLOR)

	# 	if ai_history is None:
	# 		ai_history = self._ai_history

	# 	assert(status != CONTINUE)

	# 	game_board = Board() #every game starts with the starting board

	# 	if status == WIN:
	# 		factor = WIN_FACTOR
	# 	elif status == LOSE:
	# 		factor = LOSE_FACTOR
	# 	elif status == TIE:
	# 		factor = 1
	# 		# assuming ai_history begins with the first move made
	# 	for k, move in enumerate(ai_history):
	# 		assert(game_board in game_history)

	# 		if not ai_first:
	# 			# print "ai first false"
	# 			game_board = game_board.applyMove(player_history[k])

	# 		# get the possible moves from this board in a list

	# 		game_moves = game_board.getMoveList(AI_COLOR)

	# 		# j is the index of the taken move in the list of possible moves
	# 		for j, (s_board, s_move) in enumerate(game_moves):
	# 			# if s_board == new_board:
	# 			if s_move == move:
	# 				break				


	# 		state = game_board.getArray().tolist()
	# 		# print state
	# 		state_flag = False
	# 		# if state in self.state_list:
	# 			# i is the index of the move state in the learner's state_list
	# 		for i, s_state in enumerate(self.state_list):
	# 			if len([a for a, b in zip(state, s_state) if a == b]) == len(state):
	# 				#print i, j, len(self.weights_list[i]) - 1
	# 				self.weights_list[i][j] *= factor
	# 				state_flag = True
	# 				break
				
	# 		if not state_flag:
	# 			self.state_list.append(state)
	# 			weights = [1] * len(game_moves)

	# 			weights[j] *= factor 

	# 			self.weights_list.append(weights)
				
	# 		#game_board becomes the result of the current move
	# 		test_board = game_board.applyMove(move)
	# 		if test_board is None:
	# 			game_board.printBoard()
	# 			move.printMove()
	# 			raise Exception()
	# 		game_board = game_board.applyMove(move)

	# 		if ai_first and k < len(player_history):
	# 			# print "player move applied"
	# 			game_board = game_board.applyMove(player_history[k])


	# 	# if there's a player history, we'll update the weights in a similar fashion, 
	# 	# with an inverted starting board, assuming the player_moves are already inverted
	# 	# if player_history is not None:
	# 	# 	self.updateWeights(Board(end_board.getInverse()), status = status, ai_history = player_history, player_history = ai_history, ai_first = not ai_first)
	# 	self.X = np.array(self.state_list)
	# 	self._tree = BallTree(self.X, metric='manhattan')

	def getAiHistory(self):
		return cp.deepcopy(self._ai_history)

	def _getMinimax(self, current_board):
		# return random.choice([bd[1] for bd in current_board.getMoveList(AI_COLOR)])
		(bestBoard, bestVal) = minMax2(current_board, 6)
		# print("bestVal", bestVal)
		# bestBoard[0].printBoard()
		return bestBoard[1]

	def _getNearestNeighbors(self, current_board):
		#dist, ind = self._tree.query(current_board.getArray(), k=3)
		if self._tree is None:
			return None
		ind = self._tree.query_radius(current_board.getArray(), r = self._threshold).tolist()
		ind = ind[0].tolist()

		if len(ind) > 0:
			pass
			# print "neighbors found"

		#cur_moves = current_board.getMoveList(AI_COLOR)
		moves = []
		weights = []
		# print ind
		for i in ind:
			_board = Board(new_array = self.state_list[i])
			assert(len(_board.getMoveList(AI_COLOR)) == len(self.weights_list[i]))
			for j, (board, move) in enumerate(_board.getMoveList(AI_COLOR)):
				# move.printMove()
				# current_board.printBoard()
				if current_board.verifyMove(AI_COLOR, move = move):
					# print "move found"
					# move.printMove()
					if move not in moves:
						moves.append(move)
						weights.append(self.weights_list[i][j])
					else:
						weights[moves.index(move)] *= self.weights_list[i][j]
		if len(moves) == 0:
			# raise Exception()
			# print "aborted neighbors"
			return None
		else:
			assert(len(moves) == len(weights))
			zipped = zip(moves, weights)
			moves = [mv[0] for mv in zipped if mv[1] >= 1]
			weights = [mv[1] for mv in zipped if mv[1] >= 1]

			if len(moves) < 1: return None

			return np.random.choice(moves, 1, weights)[0]
		#neighbor_moves = [move for move in neighbor_moves if move in cur_moves]


	def _featureTransform(self):
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
        return (board, np.sum(board.getArray()))

    # So we are not at an end node, now we need to do minmax
    # Set up values for minmax
    best_move_value = bestMove
    best_board = None

    # MaxNode
    if bestMove == float('-inf'):
        # Create the iterator for the Moves
        board_moves = board.getMoveList(AI_COLOR)
        for board_move in board_moves:

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


    # Things appear to be fine, we should have a board with a good value to move to
    return (best_board, best_move_value)




#http://scikit-learn.org/stable/modules/neighbors.html#classification
#http://www.sciencedirect.com/science/article/pii/S0925231210003875
