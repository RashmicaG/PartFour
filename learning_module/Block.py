#Block

class Block:
	def __init__(self, label, block_status, block_shape, block_size, block_colour, supporting_block = None):
		self.label = label
		self.block_status = block_status
		self.block_shape = block_shape
		self.block_size = block_size
		self.block_colour = block_colour
		self.supporting_block = supporting_block
	#getters	
	def getLabel(self):
		return self.label
	def getStatus(self):
		return self.block_status
	def getShape(self):
		return self.block_shape
	def getSize(self):
		return self.block_size
	def getColour(self):
		return self.label
	def getSupportingBlock(self):
		return self.supporting_block
	#setters	
	def setStatus(self, block_status):
		self.block_status = block_status
	def setSupportingBlock(self, supporting_block):
		self.supporting_block = supporting_block
	
