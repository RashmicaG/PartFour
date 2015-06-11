#include <iostream>
using namespace std;

enum block_status{ON_TABLE, PICKED_UP, ON_BLOCK};
enum block_shape{PRISM, CUBOID, CUBE};
enum block_size{SMALL, MEDIUM, LARGE};
enum block_colour{RED, GREEN, BLUE};
enum Action{PICK_UP, PUT_DOWN}
class Block{
	Block supporting_block = null;
	int name;
	block_status status;
	block_shape shape;
	block_size size;
	block_colour colour;
	public:
		//Contructors
		Block(block_status, block_shape, block_size, block_colour);
		Block(Block,block_status, block_shape, block_size, block_colour);
		//Getters
		block_status getBlockStatus(){return status};
		block_shape getBlockShape(){return shape};
		block_size getBlockSize(){return size};
		block_colour getBlockColour(){return colour};
		//Setters
		void setBlockStatus(block_status b_status){status = b_status};		
		void setBlockShape(block_shape b_shape){shape = b_shape};
		void setBlockSize(block_size b_size){size = b_size};
		void setBlockColour(block_colour b_colour){colour = b_colour};
}
//Constructors
Block::Block(block_status stat, block_shape shap, block_size siz, block_colour col): status(stat), shape(shap), size(siz), colour(col){}
Block::Block(Block supporting,block_status, block_shape, block_size, block_colour): supporting_block(supporting), status(stat), shape(shap), size(siz), colour(col){}

class State_Action{
	float Q_value;
	float transition_probablity;
	Block actionable_block;
	Action action;
	State nextState;
	public:
		// Constructor
		State_Action(float, float, Block, Action, State);
		// Getters
		float getQValue(){return Q_value};
		float getTransitionProbablity(){return transition_probablity};
		Block getActionableBlock(){return actionable_block};
		Action getAction(){return action};
		State getNextState(){return nextState};
		// Setters
		void setQValue(float value){ Q_value = value};
		void setTransitionProbablity(float tp_value){transition_probablity = tp_value};
}
//Constructors
State_Action::State_Action(float Q_val, float trans_prob, Block block, Action act, State state): Q_value(Q_val), transition_probablity(trans_prob), 
actionable_block(block), action(act), nextState(state) {}

class Configuration{
	// Actionable blocks are any block that you can pickup and put down. 
	// Does not contain block that has a block on top of it.
	int num_actionable_blocks; 
	Block* actionable_blocks;
	public:
		//Constructors
		Configuration(int, Block*);
		//Getters
		int getNumActionableBlocks(){return num_actionable_blocks);
		Block* getActionableBlockArray(){return actionable_blocks};
		
}
//Constructors
Configuration::Configuration(int numBlocks, Block* blockArray): num_actionable_blocks(numBlocks), actionable_blocks = blockArray{}


class State{
	Configuration block_configuration;
	float reward;
	State_Action actions[];
	public:
		//Constructors
		State(Configuration, float, int, State_Action);
		//getter
		Configuration getBlockConfiguration(){return block_configuration};
		float getReward(){return reward};
		State_Action getStateActions(){return actions}; 
		//setter
		void setReward(float r){reward = r};
}
//Constructors
State::state(Configuration lastConfig, float rew, int, State_Action act): reward(rew){
	//Work out next state
}

class MDP{
	State initial_state;
}

int main (){
  
}
