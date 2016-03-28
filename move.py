import numpy as np
import copy as cp
from globalconsts import \
	EMPTY, RED, BLACK, BKING, RKING, \
	FORWARD_LEFT, FORWARD_RIGHT, BACKWARD_LEFT, BACKWARD_RIGHT


class Move(object):
	'''A class to represent a Move, i.e. a chain of piece coordinate updates and Boards'''
	def __init__(self, board = None, piece = None, direction = None):
		self.__move_chain = []
		self.__piece = piece
		self.__board = board

		
		pass

	def update(self, direction):



