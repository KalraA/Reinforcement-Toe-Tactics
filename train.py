from ttt import Game
from train_bot import Bot, RandBot
import numpy as np
epochs = 500
games_per_epoch = 10
total_memory = []

def process_replay(replay, result, bot=None):
	X_data = []
	Y_data = []
	res = result
	discount = .95
	if res == 0.5:
		discount = 1
	for i in reversed(range(len(replay)-1)):
		player = 0
		move = -1
		for j in range(9):
			if replay[i][j] != replay[i+1][j]:
				player = replay[i+1][j]
				move = j
				break;
		X = [0, 0, 0, 0, 0, 0, 0, 0, 0]
		for j in range(9):
			if replay[i][j] == ' ':
				X[j] = 0
			elif replay[i][j] == player:
				X[j] = 1
			else:
				X[j] = -1
		Y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
		Y[move] = res
		res *= discount
		X_data.append(X)
		Y_data.append(Y)
		if res != 0.5:
			res *= -1
	return X_data, Y_data

X_train = []
Y_train = []
for epoch in range(0, epochs):
	# bot = Bot(450 + epoch)
	# X_train = []
	# Y_train = []
	for game in range(games_per_epoch):
		# bot2 = RandBot(epoch)
		# bot2 = 'rand'
		rand_move = 9
		current_game = Game(rand_move, 0, 0);
		current_game.start_game()
		replay = current_game.get_game()
		result = current_game.get_reward()
		X_data, Y_data = process_replay(replay, result)
		# print replay
		X_train += X_data
		Y_train += Y_data
		# print(X_train)
		# print(Y_train)
	# bot.train(X_train, Y_train)
	# bot.save_model()
	print epoch

def accuracy(bott):
	predictions = bott.model.predict(X_test)
	right = 0
	wrong = 0
	for i in range(len(predictions)):
		if np.argmax(Y_test[i]) == np.argmax(predictions[i]):
			right += 1
		else:
			wrong += 1
	print right
	print right + wrong
	print wrong

bot = Bot(0);
test_size = 0.15
X_test = np.array(X_train[int(len(X_train)*(1-test_size)):len(X_train)])
Y_test = np.array(Y_train[int(len(X_train)*(1-test_size)):len(X_train)])
for i in range(450):
	print i
	bot.model.fit(np.array(X_train[0:int(len(X_train)*(1-test_size))]), np.array(Y_train[0:int(len(X_train)*(1-test_size))]), nb_epoch=1, batch_size=1024, validation_split=0.05)
	bot.save_model()
	bot = Bot(i+1)
	accuracy(bot)


for epoch in range(0, epochs):
	bot = Bot(epoch)
	X_train = []
	Y_train = []
	for game in range(games_per_epoch):
		bot2 = RandBot(epoch)
		bot2 = 'rand'
		rand_move = 2//(epochs//40)
		current_game = Game(rand_move, 0, 0);
		current_game.start_game()
		replay = current_game.get_game()
		result = current_game.get_reward()
		X_data, Y_data = process_replay(replay, result)
		# print replay
		X_train += X_data
		Y_train += Y_data
		# print(X_train)
		# print(Y_train)
	bot.train(X_train, Y_train)
	bot.save_model()
	print epoch



