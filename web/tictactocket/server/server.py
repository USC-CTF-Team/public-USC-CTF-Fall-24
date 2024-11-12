from flask import Flask, render_template, session
from flask_socketio import SocketIO, send, emit
from game import Game
from datetime import timedelta
from time import sleep
from secrets import token_hex

app = Flask(__name__)
app.config['SECRET_KEY'] = str(token_hex())
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)
socketio = SocketIO(app)

#game_dict = dict()

def get_game(json):
    # if "game_id" in json and json["game_id"] in game_dict:
    #     return game_dict[json["game_id"]]
    # return None

    if type(json) is dict and "game_id" in json and json["game_id"] in session:
        return session[json["game_id"]]
    if type(json) is str and json in session:
        return session[json]
    return None

@app.route("/")
def main_page():
    session.permanent = True
    return render_template("tictactoe.html")

@socketio.on('client_new_game')
def new_game():
    newGame = Game()
    #print('New game started:' + newGame.game_id)
    emit('server_new_game', {"game_id": newGame.game_id})
    session[newGame.game_id] = newGame
    board_update(newGame.game_id)

def board_update(game_id):
    game = get_game(game_id)
    if game is not None:
        winner = game.get_winner()
        if winner == 0:
            with open("flag.txt", "r") as f:
                emit('server_board_update', {"is_valid": True, "board": game.board, "winner": winner, "flag": f.readline()})
        else:
            emit('server_board_update', {"is_valid": True, "board": game.board, "winner": winner, "turn": game.turn})
        if game.get_winner() >= 0:
            session.pop(game_id)
    else:
        emit('server_board_update', {"is_valid": False})

    

@socketio.on('client_check_square_valid')
def check_square_valid(json):
    is_valid = False
    square = -1
    game = get_game(json)
    if game is not None and "square" in json:
        square = json["square"]
        if game.is_valid_placement(json["square"]):
            is_valid = True
    emit("server_check_square_valid", {"is_valid": is_valid, "square": square})

@socketio.on('client_place_square')
def place_square(json):
    game = get_game(json)
    if game is not None and "square" in json:
        game.place_square(json["square"], 0)
        board_update(json["game_id"])
        sleep(3)
        game.place_square(game.computer_move(), 1)
        board_update(json["game_id"])

if __name__ == '__main__':
    socketio.run(app)