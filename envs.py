import random
import sys
import copy
import numpy as np

class TicTacToe:
    def __init__(self):
        self.name = 'TicTacToe'
        self.board = [' '] * 9
        self.state = np.zeros((18))
        self.bot_marker = 'O'
        self.player_marker = 'X'
        self.winning_combos = (
        [6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    )
        self.form = '''
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           '''                 

    def print_board(self,board = None):
        "Display board on screen"
        if board is None:
            print self.form % tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])
        else:
            # when the game starts, display numbers on all the grids
            print self.form % tuple(board[6:9] + board[3:6] + board[0:3])

    def is_winner(self, state):
        "check if this marker will win the game"
        # order of checks:
        #   1. across the horizontal top
        #   2. across the horizontal middle
        #   3. across the horizontal bottom
        #   4. across the vertical left
        #   5. across the vertical middle
        #   6. across the vertical right
        #   7. across first diagonal
        #   8. across second diagonal
        for i in range(2):
            board = state[i*9:9*(i+1)]
            for combo in self.winning_combos:
                if (board[combo[0]] == board[combo[1]] == board[combo[2]] == 1):
                    return i
        return -1

    def get_bot_move(self):
        '''
        find the best space on the board for the bot. Objective
        is to find a winning move, a blocking move or an equalizer move. 
        Bot must always win
        '''
        # check if bot can win in the next move
        # for i in range(0,len(self.board)):
        #     board_copy = copy.deepcopy(self.board)
        #     state_copy = copy.deepcopy(self.state)
        #     if self.is_space_free(board_copy, i):
        #         self.make_move(board_copy, state_copy, i,self.bot_marker)
        #         if self.is_winner(state_copy) == 1:
        #             return i
        # # check if player could win on his next move
        # for i in range(0,len(self.board)):
        #     board_copy = copy.deepcopy(self.board)
        #     state_copy = copy.deepcopy(self.state)
        #     if self.is_space_free(board_copy, i):
        #         self.make_move(board_copy, state_copy, i,self.player_marker)
        #         if self.is_winner(state_copy) == 0:
        #             return i

        # check for space in the corners, and take it
        # move = self.choose_random_move(range(9))
        move = 0;
        while self.board[move] != ' ':
            move += 1
        if move != None:
            return move

    def is_space_free(self, board, index):
        "checks for free space of the board"
        # print "SPACE %s is taken" % index
        return board[index] == ' '

    def is_board_full(self):
        "checks if the board is full"
        if sum(self.state) == 9:
            return True
        return False

    def make_move(self, board, state, index, move):
        board[index] =  move
        if move == 'X':
            state[index] = 1
        else:
            state[9+index] = 1

    def render(self):
        self.print_board()

    def reset(self):
        self.board = [' '] * 9
        self.state = np.zeros((18))
        self.fmove = int(random.random()*2)
        self.start()
        legal_moves = []
        for i in range(len(self.board)):
            if self.board[i] == ' ':
                legal_moves.append(i)
        # print legal_moves
        return self.state, legal_moves

    def start(self):
        if self.fmove == 1:
            move = self.get_bot_move()
            self.make_move(self.board, self.state, move, self.bot_marker)

    def step(self, action):
        done = 0
        # print self.board
        if self.board[action] != ' ':
            return False, -1, []
        self.make_move(self.board, self.state, action, self.player_marker)
        # self.rotate_board(self.board, self.state)
        win = self.is_winner(self.state)
        # print self.state
        if win == 0: #player win
            done = 1
        elif win == 1: #bot win
            done = 2
        elif self.is_board_full(): # draw
            done = 3
        if done > 0:
            return self.state, done, []
        move = self.get_bot_move()
        self.make_move(self.board, self.state, move, self.bot_marker)
        # self.rotate_board(self.board, self.state)
        # self.render()      
        win = self.is_winner(self.state)
        if win == 0:
            done = 1
        elif win == 1:
            done = 2
        elif self.is_board_full():
            done = 3
        legal_moves = []
        # if done == 3:
        #     self.render()
        for i in range(len(self.board)):
            if self.board[i] == ' ':
                legal_moves.append(i)
        return self.state, done, legal_moves

    def choose_random_move(self, move_list):
        possible_winning_moves = []
        for index in move_list:
            if self.is_space_free(self.board, index):
                possible_winning_moves.append(index)
        if len(possible_winning_moves) != 0:
            return random.choice(possible_winning_moves)
        else:
            return None

    def rotate_board(self, board, state):
        lst = []
        for i in range(0, 4):
            new_board = copy.deepcopy(board)
            new_state = copy.deepcopy(state)
            for j in range(i):
                new_board = self.rotate(board)
                new_state = self.rotate(new_state[0:9]) + self.rotate(new_state[9:18])
            lst.append((new_board + [i], new_state + [i]))
        lst.sort()
        self.board = lst[0][0][:9]
        self.state = np.array(lst[0][1][:18])

    def rotate(self, arr):
        new_arr = [0]*9
        for i in range(len(new_arr)):
            new_arr[i] = arr[i//3 + 3*(2 - (i)%3)]
        return new_arr

# 0 1 2
# 3 4 5
# 6 7 8

# 6 3 0
# 7 4 1
# 8 5 2
# env = TicTacToe()
# done = 1
# while True:
#     if done > 0:
#         state = env.reset()
#         print done
#     done = -1
#     env.render()
#     while done == -1:
#         action  = int(raw_input())
#         state, done = env.step(action)
#     print state

