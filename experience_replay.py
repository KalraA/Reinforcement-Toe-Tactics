import random
import copy
class ER:
	def __init__(self, max_len=100):
		self.replay = []
		self.max_len = 100
		self.curr_game = []

	def store(self, state, action, reward, next_state):
		self.curr_game.append((state, action, reward, next_state))
		discount = 0.97
		if reward != 0:
			r_0 = 0
			i = 0
			for s, a, r, _s in reversed(self.curr_game):
				# print 'store'
				# print a
				# r_0 = r + discount*r_0
				self.replay.append((s, a, r, _s))

			while len(self.replay) > self.max_len:
				self.replay.pop()
			self.curr_game = []

	def get_random_minibatch(self, size=10):
		# print self.replay
		if len(self.replay) > size:
			copied = copy.deepcopy(self.replay)
			random.shuffle(copied)
			return copied[:size]
		else:
			return self.replay