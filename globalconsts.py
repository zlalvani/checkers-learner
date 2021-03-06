# piece names
BKING = -2
BLACK = -1
EMPTY = 0
RED = 1
RKING = 2
AI_COLOR = RED
PLAYER_COLOR = BLACK

#directions
FORWARD_LEFT = 1
FORWARD_RIGHT = 2
BACKWARD_LEFT = 3
BACKWARD_RIGHT = 4

#threshold of distance to switch between NN and minimax
THRESHOLD = 10

#Factors to scale weights by on a win or loss. These should be reciprocals. 
WIN_FACTOR = 2.0
LOSE_FACTOR = 1.0 / WIN_FACTOR 

#Game status signifiers
WIN = 1
TIE = 0
LOSE = -1
CONTINUE = 2