#MDP
import Constants as const
from Block import Block
from Configuration import Configuration
from StateAction import StateAction
from State import State
import itertools
import copy as cp
class MDP:
	def __init__(self, label):
		self.const = const.constants()
		self.label = label
		self.statelist = []
	
	#getters and setters
	def getStateList(self):
		return self.statelist
		
	def addState(self, state):
		self.statelist.append(state)
	
	def QLearning(self, nextState, action_chosen):
		maxQ = max(act.getQValue() for act in nextState.getStateActions())
		newQval = 1
		newQval = action_chosen.getQValue() + self.const.ALPHA*(nextState.getReward() + self.const.GAMMA*(maxQ - action_chosen.getQValue()))
		action_chosen.setQValue(newQval)
		
	#Creates new configuration given the previous state and chosen action.
	def createConfiguration(self, prevState, action_chosen):
		blocks = cp.deepcopy(prevState.getConfiguration().getAllBlocks())
		for block in blocks:
			if block.getLabel() == action_chosen.getActionBlock().getLabel():
				if action_chosen.getAction() == const.Action.PICK_UP:
					block.setStatus(const.block_status.STATUS_IN_ARM)
					block.setSupportingBlock(None)
				else:
					if action_chosen.getDestination() == const.Destination.DEST_ON_TABLE:
						block.setStatus(const.block_status.STATUS_ON_TABLE)
						block.setSupportingBlock(None)
					else:
						block.setStatus(const.block_status.STATUS_ON_BLOCK)
						block.setSupportingBlock(action_chosen.getDestinationBlock())
				break
		newConfig = Configuration(blocks)
		return newConfig
		
	#Creates State given a configuration of blocks. 
	def createState(self, newConfig):
		label = len(self.statelist)
		newState = State(label, newConfig, -1.5)
		return newState
	
	# Getting the nextstate from the state list, given the action.
	def getNextState(self, currentState, action_chosen):
		for nstate in currentState.getNextStateAddress():
			for action in self.statelist[nstate].getPreviousActions():
				if action.getLabel() == action_chosen.getLabel():
					nextState = self.statelist[nstate]
					return nextState		
		return None
		
	# Finds the nextState
	def findNextState(self, currentState, action_chosen, newConfig):
		addr = 0
		for state in self.statelist:
			action_blocks = state.getConfiguration().getAllBlocks()
			same_config = True
			for ablock, cblock in itertools.izip(action_blocks, newConfig.getAllBlocks()):
				if(ablock.getStatus() != cblock.getStatus()):
					same_config = False
					break
			if(same_config):
				return [addr,state]
			addr+=1
		return [addr, None]


	def simulatorMDP(self, currentState, previous_action=None):
		goal = currentState.getReward() >= self.const.REWARD or currentState.getReward() <= self.const.COST
		#if(previous_action != None):
			#print "###############################################"
			#for block in currentState.getConfiguration().getAllBlocks():
				#print (block.getLabel(), block.getStatus())
			#print (previous_action.getActionBlock().getLabel(), previous_action.getAction(), previous_action.getDestination())
			#print "###############################################"
			
		if(not goal):
			if not currentState.getStateActions():
				currentState.createStateActions(previous_action)
			
			action_chosen = currentState.chooseStateAction()
			nextState = self.getNextState(currentState, action_chosen)
			if(nextState == None):
				newConfig = self.createConfiguration(currentState, action_chosen)
				nextState_and_addr = self.findNextState(currentState, action_chosen, newConfig)
				nextState = nextState_and_addr[1]
				address = nextState_and_addr[0]
				if(nextState == None):
					nextState = self.createState(newConfig)
					self.addState(nextState)
					address = len(self.getStateList())-1
				
				currentState.addNextStateAddress(address) 
				nextState.addPreviousActions(action_chosen)
			nextState.createStateActions(action_chosen)
			self.QLearning(nextState, action_chosen)
			self.simulatorMDP(nextState, action_chosen)
		else:
			return

block_list = []
for i in range(0,3):
	block = Block(i, const.block_status.STATUS_ON_TABLE, const.block_shape.CUBE, const.block_size.SMALL, const.block_colour.RED)
	block_list.append(block)

blocks = cp.deepcopy(block_list)
config = Configuration(blocks)
mdp = MDP(0)
initState = State(0, config, -1.5)
mdp.addState(initState)

block_list[0].setStatus(const.block_status.STATUS_ON_TABLE)
block_list[1].setStatus(const.block_status.STATUS_ON_BLOCK)
block_list[1].setSupportingBlock(block_list[0])
block_list[2].setStatus(const.block_status.STATUS_ON_BLOCK)
block_list[2].setSupportingBlock(block_list[1])
#block_list[3].setStatus(const.block_status.STATUS_ON_BLOCK)
#block_list[3].setSupportingBlock(block_list[2])
stack = Configuration(block_list)
goalState = State(1, stack, mdp.const.REWARD)
mdp.addState(goalState)
for i in range(0,1000):
	try:
		mdp.simulatorMDP(initState)
	except RuntimeError:
		print "Woopsies"
		break
	
#print len(mdp.getStateList())
#for state in mdp.getStateList():
	#for action in state.getStateActions():
		#print action.getQValue()
	#print "\n"

