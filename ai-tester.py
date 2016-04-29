import numpy as np
import copy as cp
from board import Board
from learner import Learner
from move import Move
from globalconsts import RED, BLACK, AI_COLOR, PLAYER_COLOR, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT, \
	WIN, CONTINUE, LOSE, TIE


if __name__ == "__main__":

	game_count = 50

	winner = Learner()
	loser = Learner()
	# game_board = Board()

	for game in range(game_count):
		game_board = Board()

		winner_moves = []
		loser_moves = []
		game_history = []

		turn_count = 0

		tie_flag = False

		while game_board.checkGameStatus(AI_COLOR) == CONTINUE:

			if turn_count > 100:
				tie_flag = True
				break


			loser_move = loser.getNextMove(game_board.getInverse())

			loser_moves.append(loser_move.getInverse())
			assert(loser_move is not None and game_board is not None)
			game_history.append((game_board, loser_move.getInverse()))

			# loser_move.printMove()
			loser_move.getInverse().printMove()

			# game_board.printBoard()
			# temp = game_board
			game_board.printBoard()
			game_board = Board(game_board.applyMove(loser_move.getInverse()))
			game_board.printBoard()
			# assert(temp != game_board)

			# loser_move.getInverse().printMove()

			print turn_count

			# game_board.printBoard()


			if game_board.checkGameStatus(AI_COLOR) == LOSE:
				break

			# assert (temp != game_board)
			winner_move = winner.getNextMove(game_board)
			assert(winner_move is not None and game_board is not None)
			game_history.append((game_board, winner_move))

			winner_move.printMove()

			winner_moves.append(winner_move)

			# temp = game_board
			game_board = Board(game_board.applyMove(winner_move))
			# game_history.append(game_board)

			# game_board.printBoard()
			turn_count += 1


			
		print game
		if not tie_flag and game_board.checkGameStatus(AI_COLOR) != TIE:
			winner.updateWeights(game_history, status = game_board.checkGameStatus(AI_COLOR))
			# winner.updateWeights(game_board, loser_moves, winner_moves, game_history = game_history)
		else:
			winner.updateWeights(game_history, status = TIE)
			# game_board.printBoard()
			# winner.updateWeights(game_board, loser_moves, winner_moves, status = TIE, game_history = game_history)
		loser_moves = None
		winner_moves = None
	