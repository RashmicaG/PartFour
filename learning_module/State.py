#States
import Constants as const
import Block
import Configuration
import StateAction
import math
import random as rand
class State:
	#Constructor
	def __init__(self, label, block_configuration, reward):
		self.constants = const.constants()
		self.label = label
		self.block_configuration = block_configuration
		self.reward = reward
		self.previous_actions = []
		self.actions = []
		self.next_state_addr = []
	#getters
	def getLabel(self):
		return self.label
	def getConfiguration(self):
		return self.block_configuration
	def getReward(self):
		return self.reward
	def getStateActions(self):
		return self.actions
	def getPreviousActions(self):
		return self.previous_actions
	def getNextStateAddress(self):
		return self.next_state_addr
	#setters
	def setReward(self, reward):
		self.reward = reward
	#Add to lists
	def addPreviousActions(self, action):
		self.previous_actions.append(action)
	
	## The address is being added but outputting an empty list
	def addNextStateAddress(self, state_addr):
		self.next_state_addr.append(state_addr)
		
	# Create State Actions depending on what the previous action was
	def createStateActions(self, previous_action):
		i = self.label
		Q_value = -0.2
		trans_prob = 0.0
		if(previous_action == None or previous_action.getAction() == const.Action.PUT_DOWN):
			for action_block in self.block_configuration.getActionBlocks():
				action = StateAction.StateAction(i, Q_value, trans_prob, action_block, const.Action.PICK_UP)
				self.actions.append(action)
				i+=1
		elif(previous_action.getAction() == const.Action.PICK_UP):
				action = StateAction.StateAction(i, Q_value, trans_prob, previous_action.getActionBlock(), const.Action.PUT_DOWN)
				self.actions.append(action)
				for action_block in self.block_configuration.getActionBlocks():
					if(action_block.getLabel() != previous_action.getActionBlock().getLabel()):
						i+=1
						action = StateAction.StateAction(i, Q_value, trans_prob, previous_action.getActionBlock(), const.Action.PUT_DOWN, action_block)
						self.actions.append(action)
	# Calculating the transition probablities depending on the Current Q_value of State_Action pair
	def calculateTransitionProbablities(self):
		sum_val = 0.0
		for a in self.actions:
			sum_val += math.pow(self.constants.TEMPERATURE, -1*a.getQValue())
		for a in self.actions:
			prob = math.pow(self.constants.TEMPERATURE, -1*a.getQValue())/sum_val
			a.setTransitionProbablity(prob)
	# Choosing a State Action stochastically
	def chooseStateAction(self):
		chance = 0.0
		rand_num = rand.random()
		self.calculateTransitionProbablities()
		for a in self.actions:
			chance += a.getTransitionProbablity()
			if(rand_num < chance):
				return a
		print "Error in Choosing an action"




