#include <iostream>
#include <stddef.h>
#include <vector>


using namespace std;

enum block_status{ON_TABLE, PICKED_UP, ON_BLOCK};
enum block_shape{PRISM, CUBOID, CUBE};
enum block_size{SMALL, MEDIUM, LARGE};
enum block_colour{RED, GREEN, BLUE};
enum Action{PICK_UP, PUT_DOWN};

class Block;
class State_Action;
class Configuration;
class State;
class MDP;

class Block{
	Block* supporting_block;
	int name;
	block_status status;
	block_shape shape;
	block_size size;
	block_colour colour;
	public:
		//Contructors
		Block();
		Block(block_status, block_shape, block_size, block_colour);
		Block(Block*, block_status, block_shape, block_size, block_colour);
		//Getters
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
//Constructors
Block::Block(){}
Block::Block(block_status stat, block_shape shap, block_size siz, block_colour col): status(stat), shape(shap), size(siz), colour(col){}
Block::Block(Block* supporting,block_status stat, block_shape shap, block_size siz, block_colour col): supporting_block(supporting), status(stat), shape(shap), size(siz), colour(col){}

//class State_Action{
	//float Q_value;
	//float transition_probablity;
	//Block actionable_block;
	//Action action;
	//State* nextState;
	//public:
		//// Constructor
		//State_Action();
		//State_Action(float, float, Block, Action, State*);
		//// Getters
		//float getQValue(){return Q_value;}
		//float getTransitionProbablity(){return transition_probablity;}
		//Block getActionableBlock(){return actionable_block;}
		//Action getAction(){return action;}
		//State* getNextState(){return nextState;}
		//// Setters
		//void setQValue(float value){ Q_value = value;}
		//void setTransitionProbablity(float tp_value){transition_probablity = tp_value;}
//};
////Constructors
//State_Action::State_Action(){}
//State_Action::State_Action(float Q_val, float trans_prob, Block block, Action act, State* state): Q_value(Q_val), transition_probablity(trans_prob), 
//actionable_block(block), action(act), nextState(state) {}

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
//Constructors
Configuration::Configuration(int numBlocks, vector<Block>* blockArray){
	for (int i=0; i<numBlocks; i++){
		actionable_blocks.push_back(blockArray->at(i));
	}
}


//class State{
	//Configuration block_configuration;
	//float reward;
	//State_Action prev_action;
	//State_Action* actions;
	//int num_actions;
	//public:
		////Constructors
		//State(Configuration, State_Action*, float, int);
		//State(Configuration, float, int, State_Action, State_Action*);
		////getter
		//Configuration getBlockConfiguration(){return block_configuration;}
		//float getReward(){return reward;}
		//State_Action* getStateActions(){return actions;} 
		////setter
		//void setReward(float r){reward = r;}
//};
////Constructors
//State::State(){}
//State::State(Configuration init_config, State_Action* act, float rew, int n_actions): block_configuration(init_config), actions(act), reward(rew), num_actions(n_actions){}
//State::State(Configuration lastConfig, float rew, int n_actions, State_Action previous_act, State_Action* act): reward(rew), prev_action(previous_act), num_actions(n_actions){}

//class MDP{
	////State initial_state;
	////Block block[3];
	//public:
	//MDP(){
		////Block block_array[0] = new Block(ON_TABLE, CUBOID, MEDIUM, RED); 
	
		////Configuration config = new Configuration(3, block_array);
	//}
//};

int main (){
//  new MDP();
	vector<Block> block_array(1, Block(ON_TABLE, CUBOID, MEDIUM, RED));
	block_array.push_back(Block(&block_array[0],ON_BLOCK, CUBOID, MEDIUM, RED));
	block_array.push_back(Block(ON_TABLE, PRISM, LARGE, GREEN));
	block_array.push_back(Block(ON_TABLE, CUBE, SMALL, BLUE));
	
	Configuration config(block_array.size(), &block_array);
	cout<<config.getActionableBlockArray()->at(1).getBlockStatus()<<endl;
}
