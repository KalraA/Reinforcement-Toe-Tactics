from experience_replay import ER
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import rmsprop
from keras.regularizers import l2
from collections import deque
from envs import TicTacToe
import numpy as np
import random
max_len = 100
experience_replay = ER(max_len)
env = TicTacToe()
# C is the number of timesteps we update the frozen model
C = 50

training_model = Sequential()
training_model.add(Dense(20, input_dim=18))
training_model.add(Activation('relu'))
training_model.add(Dense(20))
training_model.add(Activation('relu'))
training_model.add(Dense(9))
training_model.add(Activation('linear'))
training_model.compile(loss='mse', optimizer = 'rmsprop', metrics=['accuracy'])

frozen_model = Sequential()
frozen_model.add(Dense(20, input_dim=18))
frozen_model.add(Activation('relu'))
frozen_model.add(Dense(20))
frozen_model.add(Activation('relu'))
frozen_model.add(Dense(9))
frozen_model.add(Activation('linear'))
frozen_model.compile(loss='mse', optimizer = 'rmsprop')

max_episodes = 1000
max_steps = 5
ills = 0
discount = 0.97
scores= deque(maxlen=100)

def clip(x):
	if x > 1:
		return 1
	elif x < -1:
		return -1
	else:
		return x

epsilon = 1.0
eps = 0
moves = 0
for episode in xrange(max_episodes):
	#initialize
	state, legal_moves = env.reset()

	#frozen model update
	if episode % C == 0:
		training_model.save_weights('weights.h5', overwrite=True)
		frozen_model.load_weights('weights.h5')
		frozen_model.compile(loss='mse', optimizer ='rmsprop')
		# print 'lol'
		# print frozen_model.predict(np.array([[0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1]]))
		# print training_model.predict(np.array([[0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1]]))

	#progress
	if episode % 99 == 0:
		print 'Win Rate:'
		print sum(scores)
		print 'Illegal Moves:'
		print ills
		print eps
		print moves
		ills = 0
	#play a game
	for timestep in xrange(max_steps):
		inp = np.array([state])
		preds = training_model.predict(inp)[0]
		a = random.random()
		# print a
		if a < epsilon:
			# print 'eps'
			eps += 1
			action = env.choose_random_move(range(9))
		else:
			#print inp
			action = np.argmax(preds)
			moves += 1
		epsilon = max(epsilon*0.995, 0.1)
		if episode % 10 == 0:
			print action
			print preds
		next_state, done, legal_moves = env.step(action)
		if episode % 10 == 0:
			env.render()
		#get reward
		reward = 0
		if done == -1:
			reward = -1
			scores.append(0)
			ills += 1
		elif done == 2:
			reward = -1
			scores.append(0)
		elif done == 1:
			reward = 1
			print 'ya'
			scores.append(1)
		elif done == 3:
			reward = 0.75
			scores.append(0.5)
		# if episode % 20 == 0:
		# 	print reward
		experience_replay.store(state, preds, reward, next_state)
		replay = experience_replay.get_random_minibatch(32)
		X = np.array(map(lambda x: x[0], replay))
		# print X
		# print X
		y = []
		i = 0
		r = 0
		for s, a, r, _s in replay: #state action reward next_state
			# print _s
			if r == 0.0:
				print r
				print _s
				r = np.max(frozen_model.predict(np.array([_s]))) + r
			if episode % 10 == 11:
				print 'b4'
				print a
				print 'rew'
				print r
				a[np.argmax(a)] = r
				print 'aftr'
				print a
			else:
				b = training_model.predict(np.array([s]))[0]
				b[np.argmax(a)] = clip(r)
			# print r
			y.append(a)
			i += 1
		y = np.array(y)
		state = next_state
		if len(X) > 0:
			training_model.train_on_batch(X, y)
		if done != 0:
			break;

