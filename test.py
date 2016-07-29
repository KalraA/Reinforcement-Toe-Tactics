#from train import epochs
from train_bot import Bot
from ttt import Game

bot = Bot(7)
while True:
	game = Game(0, bot, 'user')
	game.start_game()