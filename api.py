import json
from flask import Flask, request

app = Flask(__name__, static_url_path='')

@app.route('/verify', methods=['POST'])
def verify_move():
    content = request.json
    # verified  = get_next_move();
    verified = True
    return json.dumps(verified)

@app.route('/getAIMove', methods=['GET'])
def get_AI_move():
    print("here")
    # move  = get_next_move();
    move = True
    return json.dumps(move)

if __name__ == '__main__':
    app.run(debug=True)
