from collections import deque

from REINFORCE import PolicyGradientREINFORCE
import tensorflow as tf
import numpy as np
from envs import TicTacToe

env = TicTacToe()

sess = tf.Session()
optimizer = tf.train.RMSPropOptimizer(learning_rate=0.0001, decay=0.9)
writer = tf.train.SummaryWriter("logs/")

state_dim = 18
num_actions = 9

def policy_network(states):
  # define policy neural network
  W1 = tf.get_variable("W1", [state_dim, 20],
                       initializer=tf.random_normal_initializer())
  b1 = tf.get_variable("b1", [20],
                       initializer=tf.constant_initializer(0))
  h1 = tf.nn.relu(tf.matmul(states, W1) + b1)
  W2 = tf.get_variable("W2", [20, num_actions],
                       initializer=tf.random_normal_initializer(stddev=0.1))
  b2 = tf.get_variable("b2", [num_actions],
                       initializer=tf.constant_initializer(0))
  p = tf.matmul(h1, W2) + b2
  return p

pg_reinforce = PolicyGradientREINFORCE(sess,
                                       optimizer,
                                       policy_network,
                                       state_dim,
                                       num_actions,
                                       summary_writer=writer)

MAX_EPISODES = 100000
MAX_STEPS = 5
scores= deque(maxlen=100)
ills = 0
for i_episode in xrange(MAX_EPISODES):
	#initalize
	state, legal_moves = env.reset()
	for t in xrange(MAX_STEPS):
		# if i_episode % 10 == 0:
	 	# env.render()
		action = pg_reinforce.sampleAction(state[np.newaxis,:], legal_moves)
		next_state, done, legal_moves = env.step(action)
		# print legal_moves
		reward = -0.1
		if done == -1:
			reward = 0.4
			scores.append(0)
			ills += 1
			# env.render()
			# print legal_moves
		elif done == 2:
			# reward = +1
			scores.append(0)
		elif done == 1:
			# reward = -1
			scores.append(1)
		elif done == 3:
			# reward = -.5
			scores.append(0.5)

		pg_reinforce.storeRollout(state, action, reward)
		state = next_state
		if done != 0:
			break;

	pg_reinforce.updateModel()
	if i_episode % 100 == 0:
		print("Episode {}".format(i_episode))
		print("Ills {}".format(ills))
		ills = 0
		print("Finished after {} timesteps".format(t+1))
		print("Reward for this episode: {}".format(reward))
		print("Average reward for last 100 episodes: {}".format(sum(scores)))
		if sum(scores) > 80 and len(scores) >= 100:
			print("Environment {} solved after {} episodes".format('TIC TAC TOE', i_episode+1))
			break
