from board import Board
from learner import Learner
from move import Move
import unittest as ut
from globalconsts import RED, BLACK, AI_COLOR, PLAYER_COLOR, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT
from exampleboards import *


class BoardTestCase(ut.TestCase):
	def setUp(self):
		self.board = Board()

	def tearDown(self):
		self.board = None

	def testGetMovesList(self):

		def testWithGrid(grid = None, red_c = 7, black_c = 7):
			self.board = Board(new_grid = grid)
			self.board.getMoveList(RED)
			self.board.getMoveList(BLACK)

			# self.board.printBoard()
			# print "red moves:", len(self.board.getMoveList(RED))
			# print "black moves:", len(self.board.getMoveList(BLACK))

			self.assertEqual(len(self.board.getMoveList(RED)), red_c, \
				'incorrect number of RED moves available')

			self.assertEqual(len(self.board.getMoveList(BLACK)), black_c, \
				'incorrect number of BLACK moves available')

			# for board, move in self.board.getMoveList(BLACK) + self.board.getMoveList(RED):
				# print
				# move.printMove()
				# board.printBoard()


		# ---------- My Testing -----------------
		# self.board = Board(new_grid = RED_EASY_LOOKAHEAD)
		# for bd in self.board.getMoveList(RED):
		# 	bd[0].printBoard()


		testWithGrid()
		testWithGrid(KINGS, 6, 1)
		testWithGrid(CORNER, 6, 2)

		self.board = Board(new_grid = NEW_KING)
		test_board = Board(new_grid = NEW_KING_RESULT)
		
		self.assertTrue(any(bd[0] == test_board for bd in self.board.getMoveList(RED)))




	def testVerifyMove(self):
		'''
		For board verify that a move is valid and in the set of moves
		'''
		# self.board = Board(new_grid = START_MOVE_B_9_13).getInverse()
		self.board.getMoveList(RED)
		self.board.getMoveList(BLACK)

		self.assertTrue(self.board.verifyMove(BLACK, next_board = Board(new_grid = START_MOVE_B_9_13)))
		self.assertTrue(self.board.verifyMove(RED, next_board = Board(new_grid = START_MOVE_R_21_17)))


class LearnerTestCase(ut.TestCase):
	def setUp(self):
		self.board = Board()
		self.learner = Learner()

	def tearDown(self):
		self.board = None
		self.learner = None

	def testMinimax(self):
		# self.board= Board(new_grid = RED_EASY_LOOKAHEAD)
		# print(self.learner.getNextMove(self.board))

		# self.board= Board(new_grid = START)
		self.board= Board(new_grid = RED_EASY_LOOKAHEAD_2)
		best = self.learner.getNextMove(self.board)


	def testNearestNeighbor(self):
		
		weights = [0] * len(self.board.getMoveList(AI_COLOR))
		weights[0] = 1
		self.learner = Learner(data_points = [(self.board.getArray().tolist(), weights)])
		
		self.assertEqual(self.learner.getNextMove(self.board), self.board.getMoveList(AI_COLOR)[0], \
				'predicted best move does not match')


class MoveTestCase(ut.TestCase):
	def setUp(self):
		piece = (0, 1, BLACK)
		direction = FORWARD_LEFT
		self.move = Move(piece, direction)

	def tearDown(self):
		self.move = None

	def testClone(self):
		self.move.add(FORWARD_RIGHT)

		new_move = self.move.clone()

		print
		print "Move:"
		self.move.printMove()
		print
		print "New Move:"
		new_move.printMove()

		self.assertTrue(self.move == new_move)

if __name__ == "__main__":


	getMovesTestCase = BoardTestCase('testGetMovesList')
	verifyMoveTestCase = BoardTestCase('testVerifyMove')

	boardTestSuite = ut.TestSuite()
	boardTestSuite.addTest(getMovesTestCase)
	boardTestSuite.addTest(verifyMoveTestCase)

	getMinimaxTestCase = LearnerTestCase('testMinimax')
	getNearestNeighborTestCase = LearnerTestCase('testNearestNeighbor')

	learnerTestSuite = ut.TestSuite()
	learnerTestSuite.addTest(getMinimaxTestCase)
	learnerTestSuite.addTest(getNearestNeighborTestCase)

	moveTestSuite = ut.TestSuite()


	alltests = ut.TestSuite([boardTestSuite, learnerTestSuite])

	ut.main()

	#https://docs.python.org/2/library/unittest.html
