import json, learner, pickle
from board import Board
from learner import Learner
from flask import Flask, request
from globalconsts import  RED, BLACK

app = Flask(__name__, static_url_path='')

@app.route('/getAIMove', methods=['GET'])
def get_AI_move():

    try:
        current_board = pickle.load(open("current_board.pkl", "rb"))
    except:
        current_board = Board()
        pickle.dump(current_board, open("current_board.pkl", "wb"))

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
    print(content)
    boardArray = [int(str(element)) for element in content['board']]
    movePiece = (int(str(content['movePiece']['index'])), int(str(content['movePiece']['value'])))
    movePositions = [(int(str(element['index'])), int(str(element['value']))) for element in content['movePositions']]
    print("move Piece", movePiece)
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

    return json.dumps(verified)


if __name__ == '__main__':
    app.run(debug=True)
