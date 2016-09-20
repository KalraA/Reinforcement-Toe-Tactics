import random
import sys
import copy
import numpy as np

class Game:
    "Tic-Tac-Toe class. This class holds the user interaction, and game logic"
    def __init__(self, randMove, bot1, bot2):
        self.name = 'Tic Tac Toe'
        self.board = [' '] * 9
        self.player_name = ''
        self.player_marker = 'X'
        self.bot_name = 'TBot'
        self.bot_marker = 'O'
        self.winning_combos = (
        [6, 7, 8], [3, 4, 5], [0, 1, 2], [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    )
        self.corners = [0,2,6,8]
        self.sides = [1,3,5,7]
        self.middle = 4
        self.bot1 = bot1
        self.bot2 = bot2
        self.randMove = randMove
        self.form = '''
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           \t-------------
           \t| %s | %s | %s |
           '''                    
        self.game = []
        self.result = 0.5
    def print_board(self,board = None):
        "Display board on screen"
        if board is None:
            print self.form % tuple(self.board[6:9] + self.board[3:6] + self.board[0:3])
        else:
            # when the game starts, display numbers on all the grids
            print self.form % tuple(board[6:9] + board[3:6] + board[0:3])

    def get_marker(self):
        marker = raw_input("Would you like your marker to be X or Y?: ").upper() 
        while marker not in ["X","Y"]:
            marker = raw_input("Would you like your marker to be X  or Y? :").upper()
        if marker == "X":
            return ('X', 'Y')
        else:
            return ('Y','X')
    

    def help(self):
        print '''
\n\t The game board has 9 sqaures(3X3).
\n\t Two players take turns in marking the spots/grids on the board.
\n\t The first player to have 3 pieces in a horizontal, vertical or diagonal row wins the game.
\n\t To place your mark in the desired square, simply type the number corresponding with the square on the grid 
 
\n\t Press Ctrl + C to quit
'''

    def quit_game(self):
        "exits game"

    def is_winner(self, board, marker):
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
        for combo in self.winning_combos:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == marker):
                return True
        return False

    def get_bot_move(self):
        '''
        find the best space on the board for the bot. Objective
        is to find a winning move, a blocking move or an equalizer move. 
        Bot must always win
        '''
        # check if bot can win in the next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.bot_marker)
                if self.is_winner(board_copy, self.bot_marker):
                    return i
                
        # check if player could win on his next move
        for i in range(0,len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy,i,self.player_marker)
                if self.is_winner(board_copy, self.player_marker):
                    return i

        # check for space in the corners, and take it
        move = self.choose_random_move(range(9))
        if move != None:
            return move


    def is_space_free(self, board, index):
        "checks for free space of the board"
        # print "SPACE %s is taken" % index
        return board[index] == ' '

    def is_board_full(self):
        "checks if the board is full"
        for i in range(1,9):
            if self.is_space_free(self.board, i):
                return False
        return True

    def make_move(self,board,index,move):
        board[index] =  move

    def choose_random_move(self, move_list):
        possible_winning_moves = []
        for index in move_list:
            if self.is_space_free(self.board, index):
                possible_winning_moves.append(index)
        if len(possible_winning_moves) != 0:
            return random.choice(possible_winning_moves)
        else:
            return None
       
    def start_game(self):
       "welcomes user, prints help message and hands over to the main game loop"
       # welcome user 
       print '''\n\t-----------------------------------
                \n\t   TIC-TAC-TOE by Mawuli Adzaku
                \n\t------------------------------------
             '''
       self.print_board(range(1,10))
       self.help()
       # self.player_name = self.get_player_name()

       # get user's preferred marker 
       # self.player_marker, self.bot_marker = self.get_marker()
       # print "Your marker is " + self.player_marker
        
       # randomly decide who can play first
       if random.randint(0,1) == 0:
           print "I will go first"
          # self.make_move(self.board,random.choice(self.corners), self.bot_marker)
           #self.print_board()
           self.enter_game_loop('b')
       else:
           print "You will go first"          
           # now, enter the main game loop
           self.enter_game_loop('h')


    def get_player_move(self):
        move = int(input("Pick a spot to move: (1-9) "))
        while move not in [1,2,3,4,5,6,7,8,9] or not self.is_space_free(self.board,move-1) :
            move = int(input("Invalid move. Please try again: (1-9) "))
        return move - 1

    def get_player_name(self):
        return raw_input("Hi, i am %s" % self.bot_name + ". What is your name? ") 

    def get_game(self):
        return self.game

    def get_reward(self):
        return self.result

    def enter_game_loop(self,turn):
       "starts the main game loop"
       is_running = True
       moves = 0
       player = turn #h for human, b for bot
       self.print_board()
       while is_running:
           self.game.append(self.board[::])
           print player
           if self.bot2 != 'user' and (moves < self.randMove or random.random() < 0.15 or (self.bot2 == 'rand' and player == 'b')):
            if player == 'h':
              player = 'b'
              marker = 'X'
            else:
              player = 'h'
              marker = 'O'
            user_input = self.get_bot_move()
            self.make_move(self.board,user_input, marker)
            moves += 1
            if(self.is_winner(self.board, marker)):
                   if marker == 'X':
                    self.result = 1
                   else:
                    self.result = 1
                   self.game.append(self.board[::])
                   self.print_board()
                   print "\n\tCONGRATULATIONS %s, YOU HAVE WON THE GAME!!! \\tn" % self.player_name
                   #self.incr_score(self.player_name)
                   is_running = False
                   #break
            else:
               if self.is_board_full():
                   self.game.append(self.board[::])
                   self.print_board()
                   print "\n\t-- Match Draw --\t\n"
                   is_running = False
           elif player == 'h':
               user_input = self.bot1.getMove(self.board[::], 'X')
               self.make_move(self.board,user_input, self.player_marker)
               if(self.is_winner(self.board, self.player_marker)):
                   self.result = 1
                   self.game.append(self.board[::])
                   self.print_board()
                   print "\n\tCONGRATULATIONS %s, YOU HAVE WON THE GAME!!! \\tn" % self.player_name
                   #self.incr_score(self.player_name)
                   is_running = False
                   #break
               else:
                   if self.is_board_full():
                       self.game.append(self.board[::])
                       self.print_board()
                       print "\n\t-- Match Draw --\t\n"
                       is_running = False
                       #break
                   else:
                       self.print_board()
                       player = 'b'
           # bot's turn to play
           else:
              if self.bot2 == 'user':
                bot_move = self.get_player_move()
              else:
                bot_move =  self.bot2.getMove(self.board[::], 'O')
              self.make_move(self.board, bot_move, self.bot_marker)
              if (self.is_winner(self.board, self.bot_marker)):
                  self.game.append(self.board[::])
                  self.print_board()
                  self.result = 1
                  print "\n\t%s HAS WON!!!!\t\n" % self.bot_name
                  #self.incr_score(self.bot_name)
                  is_running = False
                  break
              else:
                  if self.is_board_full():
                      self.game.append(self.board[::])
                      self.print_board()
                      print "\n\t -- Match Draw -- \n\t"
                      is_running = False
                      #break
                  else:
                      self.print_board()
                      player = 'h'

       # when you break out of the loop, end the game
       self.end_game()

    def end_game(self):
       print "\n\t-- GAME OVER!!!--\n\t"
       self.quit_game()



# if __name__ == "__main__":   
#      TicTacToe = Game()
#      TicTacToe.start_game()
