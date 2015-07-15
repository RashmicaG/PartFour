#StateActions
import Constants as const
class StateAction:
	def __init__(self, label,  Q_value, transition_probablity, actionable_block, action, dest_block = None):
		self.label = label
		self.Q_value = Q_value
		self.transition_probablity = transition_probablity
		self.actionable_block = actionable_block
		self.action = action
		self.dest_block = dest_block
		if(dest_block == None):
			self.destination = const.Destination.DEST_ON_TABLE
		else:
			self.destination = const.Destination.DEST_ON_BLOCK
	
	def getLabel(self):
		return self.label
	def getQValue(self):
		return self.Q_value
	def getTransitionProbablity(self):
		return self.transition_probablity
	def getActionBlock(self):
		return self.actionable_block
	def getAction(self):
		return self.action
	def getDestination(self):
		return self.destination
	def getDestinationBlock(self):
		return self.dest_block
	
	def setQValue(self, Q_value):
		self.Q_value = Q_value
	def setTransitionProbablity(self, transition_probablity):
		self.transition_probablity = transition_probablity
