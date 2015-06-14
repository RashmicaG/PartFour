#include "Block.h"
Block::Block(){}
Block::Block(int name, block_status stat, block_shape shap, block_size siz, block_colour col): label(name), status(stat), shape(shap), size(siz), colour(col){}
Block::Block(int name, Block* supporting,block_status stat, block_shape shap, block_size siz, block_colour col): label(name), supporting_block(supporting), status(stat), shape(shap), size(siz), colour(col){}
