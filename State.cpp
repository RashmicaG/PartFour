#include "State.h"

//Constructors
State::State(int state_label, Configuration init_config, float rew): 
label(state_label), block_configuration(init_config), reward(rew){}
State::State(int state_label, Configuration lastConfig, float rew, State_Action* previous_act): 
label(state_label), block_configuration(lastConfig), reward(rew), prev_action(previous_act){}

// Methods
void State::setNextStates(vector<State>* n_states){
	vector<State>::iterator it;
	for (it = n_states->begin(); it != n_states->end(); it++){
		next_states.push_back(*it);
	}
}
//Need TO be DONE//////////////////////////////////////
float State::prevQValues(){return 0.0;}
float State::calcTransitionProbability(){return 0.0;}
///////////////////////////////////////////////////////

void State::createStateActions(){
	vector<Block> state_blocks;
	vector<Block>::iterator it;
	int i = 0;
	float Q_val;
	float trans_prob;
	for(it = block_configuration.getActionableBlockArray()->begin(); it != block_configuration.getActionableBlockArray()->end(); it++){
		state_blocks.push_back(*it);
	} 
	//for(it = state_blocks.begin(); it != state_blocks.end(); it++{
		// NEED TO BE THOUGHTOUT. 
		//if(it.getBlockStatus() == PICKED_UP){
			//Q_val = State_Action::prevQValues();
			//trans_prob = State_Action::calcTransitionProbability();
			//actions.push_back(State_Action(i, Q_val, trans_prob, *it, PUT_DOWN);
		//}
		//for(int j=0; j<state_blocks.size(); j++){
			//actions.push_back(State_Action(i, Q_val, trans_prob, *it, 
		//}
	//}
}
