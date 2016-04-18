from board import Board
from learner import Learner
from move import Move
import unittest as ut
from globalconsts import RED, BLACK, AI_COLOR, PLAYER_COLOR
from exampleboards import KINGS, START_MOVE_B_9_13, START_MOVE_R_21_17

class BoardTestCase(ut.TestCase):
	def setUp(self):
		self.board = Board()

	def tearDown(self):
		self.board = None

	def testGetMovesList(self):
		self.board.getMoveList(RED)
		self.board.getMoveList(BLACK)

		self.board.printBoard()
		print "red moves:", len(self.board.getMoveList(RED))
		print "black moves:", len(self.board.getMoveList(BLACK))

		self.assertEqual(len(self.board.getMoveList(RED)), 7, \
			'incorrect number of RED moves available')

		self.assertEqual(len(self.board.getMoveList(BLACK)), 7, \
			'incorrect number of BLACK moves available')
		
		self.board = Board(new_grid = KINGS)

		#switching the order of these gives wrong results...
		self.board.getMoveList(RED)
		self.board.getMoveList(BLACK)

		self.board.printBoard()
		print "red moves:", len(self.board.getMoveList(RED))
		print "black moves:", len(self.board.getMoveList(BLACK))

		self.assertEqual(len(self.board.getMoveList(RED)), 6, \
			'incorrect number of RED moves available')

		self.assertEqual(len(self.board.getMoveList(BLACK)), 1, \
			'incorrect number of BLACK moves available')

		for board, move in self.board.getMoveList(BLACK):
			move.printMove()
			board.printBoard()
		
	def testVerifyMove(self):
		'''
		For board verify that a move is valid and in the set of moves
		'''
		#self.board = None
		#self.board = Board()
		self.board.printBoard()
		self.board.getMoveList(RED)
		self.board.getMoveList(BLACK)

		print len(self.board.getMoveList(RED))
		print len(self.board.getMoveList(BLACK))

		for board, move in self.board.getMoveList(BLACK):
		#	print
			#move.printMove()
			continue

		#print self.board.ge
		self.assertTrue(self.board.verifyMove(BLACK, next_board = Board(new_grid = START_MOVE_B_9_13)))
		self.assertTrue(self.board.verifyMove(RED, next_board = Board(new_grid = START_MOVE_R_21_17)))


class LearnerTestCase(ut.TestCase):
	def setUp(self):
		self.board = Board()
		self.learner = Learner()

	def tearDown(self):
		self.board = None

	def testMinimax(self):
		# self.learner.getNextMove(self.board)
		pass

	def testNearestNeighbor(self):
		pass
		#weights = [0] * len(self.board.getMoveList(AI_COLOR))
		#weights[0] = 1
		#self.learner = Learner(data_points = [(self.board.getArray().tolist(), weights)])
		
		#self.assertEqual(self.learner.getNextMove(self.board), self.board.getMoveList(AI_COLOR)[0], \
		#		'predicted best move does not match')

class MoveTestCase(ut.TestCase):
	def setUp(self):
		self.move = Move()

	def tearDown(self):
		self.move = None

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
