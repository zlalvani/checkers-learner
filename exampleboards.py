from globalconsts import EMPTY, RED, BLACK, RKING, BKING

#Example boards for testing

START = [
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[ BLACK,     0, BLACK,     0, BLACK,     0, BLACK,     0],
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[   RED,     0,   RED,     0,   RED,     0,   RED,     0],
	[     0,   RED,     0,   RED,     0,   RED,     0,   RED],
	[   RED,     0,   RED,     0,   RED,     0,   RED,     0]
]

START_MOVE_B_9_13 = [
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[ BLACK,     0, BLACK,     0, BLACK,     0, BLACK,     0],
	[     0, 	 0,     0, BLACK,     0, BLACK,     0, BLACK],
	[ BLACK,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[   RED,     0,   RED,     0,   RED,     0,   RED,     0],
	[     0,   RED,     0,   RED,     0,   RED,     0,   RED],
	[   RED,     0,   RED,     0,   RED,     0,   RED,     0]
]

START_MOVE_R_21_17 = [
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[ BLACK,     0, BLACK,     0, BLACK,     0, BLACK,     0],
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[ 	  0,     0,     0,     0,     0,     0,     0,     0],
	[     0,   RED,     0,     0,     0,     0,     0,     0],
	[     0,     0,   RED,     0,   RED,     0,   RED,     0],
	[     0,   RED,     0,   RED,     0,   RED,     0,   RED],
	[   RED,     0,   RED,     0,   RED,     0,   RED,     0]
]

RED_EASY_LOOKAHEAD = [
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[ BLACK,     0, BLACK,     0, BLACK,     0,     0,     0],
	[     0, BLACK,     0,     0,     0, BLACK,     0, BLACK],
	[ 	  0,     0,     0,     0,     0,     0,     0,     0],
	[     0,   RED,     0, BLACK,     0,     0,     0,     0],
	[     0,     0,   RED,     0,   RED,     0,   RED,     0],
	[     0,   RED,     0,   RED,     0,     0,     0,   RED],
	[   RED,     0,   RED,     0,   RED,     0,   RED,     0]
]

RED_EASY_LOOKAHEAD_2 = [
	[     0, BLACK,     0, BLACK,     0, BLACK,     0, BLACK],
	[ BLACK,     0, BLACK,     0,     0,     0,     0,     0],
	[     0, BLACK,     0,     0,     0, BLACK,     0, BLACK],
	[ 	  0,     0, BLACK,     0, BLACK,     0,     0,     0],
	[     0,   RED,     0,   RED,     0,     0,     0,     0],
	[     0,     0,     0,     0,   RED,     0, BLACK,     0],
	[     0,   RED,     0,   RED,     0,     0,     0,   RED],
	[     0,     0,   RED,     0,   RED,     0,   RED,     0]
]

KINGS = [
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0, RKING,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,   RED,     0,     0,     0,     0,     0,     0],
	[     0,     0, BKING,     0,     0,     0,     0,     0]
]

CORNER = [
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,   RED,     0,   RED,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,   	 0,     0,     0,     0,     0,   RED,     0],
	[     0,     0,     0,     0,     0,     0,     0, BKING]
]

NEW_KING = [
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0, BLACK,     0, BLACK,     0,     0,     0],
	[     0,     0,     0,     0,     0,   RED,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,   	 0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0]
]

NEW_KING_RESULT = [
	[     0,     0,     0, RKING,     0,     0,     0,     0],
	[     0,     0, BLACK,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0],
	[     0,   	 0,     0,     0,     0,     0,     0,     0],
	[     0,     0,     0,     0,     0,     0,     0,     0]
]
