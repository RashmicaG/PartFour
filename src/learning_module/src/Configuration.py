#Configuration

from Block import Block
import Constants as Const
import copy as cp
class Configuration:
	def __init__(self, blocks):
		###### SOME THING WRONG IS HAPPENING HERE ##########
		allblocks = blocks
		self.blocks = cp.deepcopy(blocks)
		non_actionable_blocks = []
		i = 0
		for it in allblocks:
			if(it.getStatus() == Const.block_status.STATUS_ON_BLOCK):
				non_actionable_blocks.append(it.getSupportingBlock())
		na_blocks = []
		for ab in allblocks:
			for nb in non_actionable_blocks:
				if (ab.getLabel() == nb.getLabel() and ab.getStatus() == nb.getStatus()):
					na_blocks.append(ab);
		if(na_blocks):
			for nb in na_blocks:
				allblocks.remove(nb)
				
		self.actionable_blocks = allblocks

	def getActionBlocks(self):
		return self.actionable_blocks
	def getAllBlocks(self):
		return self.blocks

