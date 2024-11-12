import uuid, random
from collections import namedtuple

def calculateWinner(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],   # horizontal
        [0,3,6], [1,4,7], [2,5,8],   # vertical
        [0,4,8], [2,4,6]
    ]
    for locs in wins:
        if (board[locs[0]] is not None and board[locs[0]] == board[locs[1]] == board[locs[2]]):
            return board[locs[0]]
    for i in range(9):
        if board[i] is None:
            return -1
    return 3

def get_threats(board, player):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],   # horizontal
        [0,3,6], [1,4,7], [2,5,8],   # vertical
        [0,4,8], [2,4,6]
    ]
    threats = []
    for locs in wins:
        this_player = 0
        empty = 0
        empty_i = -1
        for s in locs:
            if board[s] is None:
                empty += 1
                empty_i = s
            if board[s] == player:
                this_player += 1
        if this_player == 2 and empty == 1:
            threats.append(empty_i)

    return threats

BestMove = namedtuple("BestMove", "move winner")

class Game:
    def __init__(self) -> None:
        self.board = [None] * 9
        self.game_id = str(uuid.uuid4())
        self.turn = 0
        self.turn_number = 0

    def is_valid_placement(self, square: int) -> bool:
        return square >= 0 and square < 9 and self.board[square] is None
    
    def place_square(self, square: int, player: int):
        if square >= 0 and square < 9 and self.turn == player:
            self.board[square] = player
            self.turn = (self.turn + 1) % 2
            self.turn_number += 1

    def get_winner(self) -> int: 
        return calculateWinner(self.board)
    
    def computer_move(self) -> int:
        # Opening move
        if self.turn_number == 1:
            if self.board[4] != 0:
                return 4
            else:
                return random.choice([0,2,6,8])

        return self.board_eval(self.board[:], 1).move
    
    def board_eval(self, board, this_player) -> BestMove:
        other_player = 1 - this_player
        
        #print(self.turn_number, this_player, board)

        # Check if tie
        is_tie = True
        for i in range(9):
            if board[i] is None:
                is_tie = False
                break
        if is_tie:
            return BestMove(-1, 3)

        # Look for win / block
        win_threats = get_threats(board, this_player)
        if len(win_threats) > 0:
            #print("Win")
            return BestMove(win_threats[0], this_player)
        lose_threats = get_threats(board, other_player)
        if len(lose_threats) > 0:
            #print("Blocking")
            board_copy = board[:]
            board_copy[lose_threats[0]] = this_player
            if len(lose_threats) > 1:
                #print("Guaranteed loss")
                return BestMove(lose_threats[0], other_player)
            else:
                expected_winner = self.board_eval(board_copy, other_player).winner
                #print("End result:", expected_winner)
                return BestMove(lose_threats[0], expected_winner)

        # Look for fork
        for i in range(9):
            if board[i] is None:
                board[i] = 1
                my_threats = get_threats(board, 1)
                if len(my_threats) >= 2:
                    #print("Forking")
                    return BestMove(i, this_player)
                board[i] = None
                
        # Look ahead further
        best_option = BestMove(-1, other_player)
        for i in range(9):
            if board[i] is None:
                #print("What if: move", i)
                board_copy = board[:]
                board_copy[i] = this_player
                eval_result = self.board_eval(board_copy, other_player)
                if eval_result.winner == this_player:
                    #print("Guaranteed win")
                    return BestMove(i, this_player)
                elif eval_result.winner == 3:
                    best_option = BestMove(i, 3)
                elif best_option.winner == other_player:
                    best_option = BestMove(i, other_player)
        
        #print("Best option:", best_option.move, "(result:", best_option.winner, ")")
        return best_option


    