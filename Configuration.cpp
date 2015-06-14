#include "Configuration.h"
Configuration::Configuration(vector<Block>* blocks){
	vector<Block>::iterator it;
	vector<Block> non_actionable_blocks;
	for (int i=0; i<blocks->size(); i++){
		actionable_blocks.push_back(blocks->at(i));
	}
	
	for(it = actionable_blocks.begin(); it != actionable_blocks.end(); it++){
		if(it->getBlockStatus() == STATUS_ON_BLOCK){
			 non_actionable_blocks.push_back(*(it->getSupportingBlock()));
		}
	}
	for(it = non_actionable_blocks.begin(); it != non_actionable_blocks.end(); it++){
		actionable_blocks.erase(it);
	}
}
