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

#The model we care about 
training_model = Sequential()
training_model.add(Dense(20, input_dim=18))
training_model.add(Activation('relu'))
training_model.add(Dense(20))
training_model.add(Activation('relu'))
training_model.add(Dense(9))
training_model.add(Activation('linear'))
training_model.compile(loss='mse', optimizer = 'rmsprop', metrics=['accuracy'])

# Q^ or the frozen model
frozen_model = Sequential()
frozen_model.add(Dense(20, input_dim=18))
frozen_model.add(Activation('relu'))
frozen_model.add(Dense(20))
frozen_model.add(Activation('relu'))
frozen_model.add(Dense(9))
frozen_model.add(Activation('linear'))
frozen_model.compile(loss='mse', optimizer = 'rmsprop')

max_episodes = 1000 #max games
max_steps = 5 #max length of a game
ills = 0 #number of illegal moves
discount = 0.97 #gamme for gamma*Q(s', a') in the loss f'n
scores= deque(maxlen=100) #just a metric for checking scores

def clip(x): #clip reward to rannge [1, -1]
	if x > 1:
		return 1
	elif x < -1:
		return -1
	else:
		return x

epsilon = 1.0 #% of random moves
eps = 0 #number of random moves played
moves = 0 #number of non-random moves played
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
		#prep input
		inp = np.array([state])
		preds = training_model.predict(inp)[0]
		#random variable
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
		#epsilon decay until it's 0.1
		epsilon = max(epsilon*0.995, 0.1)
#		if episode % 10 == 0:
#			print action
#			print preds

		#play a move
		next_state, done, legal_moves = env.step(action)
		if episode % 10 == 0:
			env.render()
		#get reward
		reward = 0
		if done == -1: #illegal move
			reward = -1
			scores.append(0)
			ills += 1
		elif done == 2: #loss
			reward = -1
			scores.append(0)
		elif done == 1: #win
			reward = 1
			print 'ya'
			scores.append(1)
		elif done == 3: #tie
			reward = 0.75
			scores.append(0.5)
		# if episode % 20 == 0:
		# 	print reward
		experience_replay.store(state, preds, reward, next_state)
		replay = experience_replay.get_random_minibatch(5) #of size 5
		#X values are the states
		X = np.array(map(lambda x: x[0], replay))
		# print X
		# print X
		y = []
		i = 0
		r = 0
		for s, a, r, _s in replay: #state action reward next_state
			# print _s
			if r == 0.0: #update the reward if it's a non terminal step. the reward is 0 for all non terminal steps
				r = np.max(frozen_model.predict(np.array([_s]))) + r # gamma*Q(s', a)
			b = training_model.predict(np.array([s]))[0] #setting the gradient of all the non action values to 0, kinda hacky but works
			b[np.argmax(a)] = clip(r) #setting the action value to the Q value of the next state. Teaching NN to predict future Q vals
			# print r
			y.append(a)
			i += 1
		y = np.array(y)
		state = next_state
		#train the model
		if len(X) > 0:
			training_model.train_on_batch(X, y)
		if done != 0:
			break;

