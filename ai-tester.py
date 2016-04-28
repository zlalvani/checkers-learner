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
	game_board = Board()

	for game in range(game_count):
		game_board = Board()

		winner_moves = []
		loser_moves = []

		turn_count = 0

		tie_flag = False

		while game_board.checkGameStatus(AI_COLOR) != WIN \
		and game_board.checkGameStatus(AI_COLOR) != LOSE:

			if turn_count > 100:
				tie_flag = True
				break


			loser_move = loser.getNextMove(game_board.getInverse())

			loser_moves.append(loser_move.getInverse())

			# loser_move.printMove()
			# loser_move.getInverse().printMove()

			# game_board.printBoard()
			game_board = game_board.applyMove(loser_move.getInverse())

			loser_move.getInverse().printMove()

			print turn_count
			game_board.printBoard()


			if game_board.checkGameStatus(AI_COLOR) == LOSE:
				break

			winner_move = winner.getNextMove(game_board)

			winner_move.printMove()

			winner_moves.append(winner_move)

			game_board = game_board.applyMove(winner_move)
			game_board.printBoard()
			turn_count += 1


			
		if not tie_flag:
			winner.updateWeights(game_board, loser_moves, winner_moves)
		else:
			game_board.printBoard()
			winner.updateWeights(game_board, loser_moves, winner_moves, status = TIE)
		loser_moves = None
		winner_moves = None
		print game
	