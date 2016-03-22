from board import Board
import unittest as ut
from globalconsts import RED, BLACK
from exampleboards import KINGS

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

		self.board.getMoveList(RED)
		self.board.getMoveList(BLACK)

		self.board.printBoard()
		print "red moves:", len(self.board.getMoveList(RED))
		print "black moves:", len(self.board.getMoveList(BLACK))

		self.assertEqual(len(self.board.getMoveList(RED)), 6, \
			'incorrect number of RED moves available')

		self.assertEqual(len(self.board.getMoveList(BLACK)), 1, \
			'incorrect number of BLACK moves available')


	def testVerifyMove(self):
		pass

if __name__ == "__main__":

	getMovesTestCase = BoardTestCase('testGetMovesList')
	verifyMoveTestCase = BoardTestCase('testVerifyMove')

	boardTestSuite = ut.TestSuite()
	boardTestSuite.addTest(getMovesTestCase)
	boardTestSuite.addTest(verifyMoveTestCase)
	
	alltests = ut.TestSuite([boardTestSuite])

	ut.main()

	#https://docs.python.org/2/library/unittest.html