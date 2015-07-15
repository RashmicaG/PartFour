#Constants
from enum import Enum
class constants:
	def __init__(self):
		self.ALPHA = 0.5
		self.GAMMA = 1.0
		self.REWARD = 10
		self.COST = -10
		self.TEMPERATURE = 0.5
		
class block_status(Enum):
	STATUS_ON_TABLE = 0
	STATUS_IN_ARM = 1
	STATUS_ON_BLOCK = 2

class block_shape(Enum):
	PRISM = 0
	CUBOID = 1
	CUBE = 2

class block_size(Enum):
	SMALL = 0
	MEDIUM = 1
	LARGE = 2

class block_colour(Enum):
	RED = 0
	MEDIUM = 1
	LARGE = 2

class Destination(Enum):
	DEST_ON_TABLE = 0
	DEST_ON_ARM = 1
	DEST_ON_BLOCK = 2

class Action(Enum):
	PICK_UP = 0
	PUT_DOWN = 1

