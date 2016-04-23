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
        learner = pickle.load(open("learner.pkl", "rb"))
    except:
        learner = Learner()
        current_board = Board()
        pickle.dump(current_board, open("current_board.pkl", "wb"))
        pickle.dump(learner, open("learner.pkl", "wb"))

    # Use the learner to make an AI move
    # current_board.getInverse().printBoard()
    move = learner.getNextMove(current_board.getInverse())
    # print("Got move \n \n")
    move[0].printBoard()

    # next_board = move.getInverse()
    # Save move into pickle file
    # pickle.dump(next_board, open("current_board.pkl", "wb"))

    # next_board_array = next_board.getArray()
    return json.dumps(next_board_array.tolist())

@app.route('/getBoard', methods=['GET'])
def get_board():
    try:
        current_board = pickle.load(open("current_board.pkl", "rb"))
    except:
        current_board = Board()
        pickle.dump(current_board, open("current_board.pkl", "wb"))
    return json.dumps(current_board.getArray())

@app.route('/verify', methods=['POST'])
def verify_move():
    content = request.json
    boardArray = [int(str(element)) for element in content['data']]

    # try:
    #     current_board = pickle.load(open("current_board.pkl", "rb"))
    # except:
    current_board = Board()
    pickle.dump(current_board, open("current_board.pkl", "wb"))

    verified = current_board.verifyMove(RED, next_board = Board(new_array = boardArray))
    if(verified):
        pickle.dump(Board(new_array = boardArray), open("current_board.pkl", "wb"))

    print("move is ", verified)

    return json.dumps(verified)


if __name__ == '__main__':
    app.run(debug=True)
