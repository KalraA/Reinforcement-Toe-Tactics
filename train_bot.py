from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten, Reshape
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, adamax
import numpy as np
import random

class Bot:
	def __init__(self, iteration=0):
		self.model = Sequential()
		self.model.add(Dense(500, input_dim=9))
		self.model.add(Activation('relu'))
		self.model.add(Dense(250))
		self.model.add(Activation('relu'))
		self.model.add(Dense(9))
		self.model.add(Activation('softmax'))
		self.iteration = iteration
		if iteration > 0:
			self.model.load_weights('bot_weights_'+str(self.iteration)+'.h5')
		self.model.compile(loss='mse', optimizer='adamax')

	def train(self, inputs, targets):
		self.model.fit(inputs, targets, nb_epoch=10, batch_size=1024)

	def getMove(self, board, player):
		for i in range(len(board)):
			if board[i] == ' ':
				board[i] = 0;
			elif board[i] == player:
				board[i] = 1
			else:
				board[i] = -1
		prediction = self.model.predict(np.array([board]))[0]
		print prediction
		move = -1
		while (move == -1 or board[move] != 0):
			move = np.argmax(prediction)
			prediction[move] = -10
			print move
		return move

	def save_model(self):
		self.model.save_weights('bot_weights_'+str(self.iteration+1)+'.h5', overwrite=True)

class RandBot:
	def __init__(self, max_iters=0):
		self.model = Sequential()
		self.model.add(Dense(100, input_dim=9))
		self.model.add(Activation('relu'))
		self.model.add(Dense(100))
		self.model.add(Activation('relu'))
		self.model.add(Dense(9))
		self.model.add(Activation('softmax'))
		self.iteration = max_iters - int(200*random.random())
		if max_iters > 0:
			self.model.load_weights('bot_weights_'+str(self.iteration+1)+'.h5')
		self.model.compile(loss='mse', optimizer='SGD')

	def getMove(self, board, player):
		for i in range(len(board)):
			if board[i] == ' ':
				board[i] = 0;
			elif board[i] == player:
				board[i] = 1
			else:
				board[i] = -1
		prediction = self.model.predict(np.array([board]))[0]
		move = -1
		while (move == -1 or board[move] != 0):
			move = np.argmax(prediction)
			prediction[move] = -10
		return move
