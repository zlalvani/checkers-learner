import json, learner, pickle
from board import Board
from learner import Learner
from flask import Flask, request
from globalconsts import  RED, BLACK

app = Flask(__name__, static_url_path='')

@app.route('/getAIMove', methods=['GET'])
def get_AI_move():

    # Load in the crrent board if it exists
    try:
        current_board = pickle.load(open("current_board.pkl", "rb"))
    except:
        current_board = Board()
        pickle.dump(current_board, open("current_board.pkl", "wb"))

    # Load in the learner class instance if it exists
    try:
        learner = pickle.load(open("learner.pkl", "rb"))
    except:
        learner = Learner()
        pickle.dump(learner, open("learner.pkl", "wb"))

    # Use the learner to make an AI move
    move = learner.getNextMove(current_board.getInverse())
    next_board = move[0].getInverse()
    # Save move into pickle file
    pickle.dump(next_board, open("current_board.pkl", "wb"))

    next_board_array = next_board.getArray()
    return json.dumps(next_board_array.tolist())

@app.route('/getBoard', methods=['GET'])
def get_board():
    try:
        current_board = pickle.load(open("current_board.pkl", "rb"))
    except:
        current_board = Board()
        pickle.dump(current_board, open("current_board.pkl", "wb"))
    return json.dumps(current_board.getArray().tolist())

@app.route('/verify', methods=['POST'])
def verify_move():
    content = request.json
    boardArray = [int(str(element)) for element in content['board']]
    def getCoor(coor):
        return [int(str(coor['xCoor'])), int(str(coor['yCoor']))]
    startingPos = getCoor(content['movePiece']['coor'])
    movePositions = [getCoor(element['coor']) for element in content['movePositions']]
    print("Starting Piece", startingPos)
    print("move Positions", movePositions)

    try:
        current_board = pickle.load(open("current_board.pkl", "rb"))
    except:
        current_board = Board()
        pickle.dump(current_board, open("current_board.pkl", "wb"))

    next_board = Board(new_array = boardArray)

    # Make it work for moves instead of board
    # next_board = current_board.(next_board)

    verified = current_board.verifyMove(RED, next_board = next_board)
    if(verified):
        pickle.dump(Board(new_array = boardArray), open("current_board.pkl", "wb"))

    return json.dumps({'verified':verified, 'board':[1]*8})


if __name__ == '__main__':
    app.run(debug=True)
