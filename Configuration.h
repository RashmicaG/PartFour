#ifndef CONFIGURATION_H
#define CONFIGURATION_H
#include <stddef.h>
#include <vector>
#include <stdlib.h>
#include "Block.h"
using namespace std;

class Configuration{
	// Actionable blocks are any block that you can pickup and put down. 
	// Does not contain block that has a block on top of it.
	vector<Block> actionable_blocks;
	public:
		//Constructors
		Configuration(int, vector<Block>*);
		//Getters
		int getNumActionableBlocks(){return actionable_blocks.size();}
		vector<Block>* getActionableBlockArray(){return &actionable_blocks;}
		
};
#endif
