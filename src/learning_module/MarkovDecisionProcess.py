#Fresh and new Learning module

class StateAction:
	def __init__(self, label):
		self.label = label
		self.nextState = None
		self.ActionBlock = None
		self.Destination = None
		self.DestinationBlock = None

class State:
	"""
	create a new state. The state would contain the configuration of the blocks.
	this would be in an array form for each block. Configuration doesn't have anything to do with 
	block attributes. It only has information on how the blocks are arranged.
	"""
	def __init__(self, label, blocks):
		self.label = label
		self.blocks = blocks
		self.configuration  = None
	def createConfiguration(self):
		#create configuration of the blocks
		pass
	def createStateActions(self):
		#create possible actions
		pass
	def getLabel(self):
		# The label is the row and column number in the matrix.
		return self.label
		
class MDP:
	def __init__(self, label, blocks):
		self.label = label
		self.blocks = blocks
		self.q_matrix = []
		self.prob_matrix = []
		self.reward_matrix = []
	def initMDP(self, states):
		# Initialise the q_matrix all to 0 and reward_matrix to -1.
		# Initialize the Probablity matrix with equal probablity for all possible actions.
		# And 0 for all actions that are not possible.
		for i in range(0, len(states)):
			for j in range(0, len(states)):
				q_matrix.append(0.0)
				if (states[i].getStateActions()[j].
			reward_matrix.append(-1.0)
		
		
		pass
	def qLearning(self):
		# q learning.
		pass
	def setReward(self):
		# set the reward matrix
		pass
	def main(self):
		#call everything here.
		pass
