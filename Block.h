#ifndef BLOCK_H
#define BLOCK_H
#include <stddef.h>
#include <vector>
#include <stdlib.h>
#include "Constants.h"
using namespace std;

class Block{
	Block* supporting_block;
	int label;
	block_status status;
	block_shape shape;
	block_size size;
	block_colour colour;
	public:
		//Contructors
		Block();
		Block(int, block_status, block_shape, block_size, block_colour);
		Block(int, Block*, block_status, block_shape, block_size, block_colour);
		//Getters
		int getLabel(){return label;}
		block_status getBlockStatus(){return status;}
		block_shape getBlockShape(){return shape;}
		block_size getBlockSize(){return size;}
		block_colour getBlockColour(){return colour;}
		Block* getSupportingBlock(){return supporting_block;}
		//Setters
		void setBlockStatus(block_status b_status){status = b_status;}
		//Initializers
		//void 
};
#endif
