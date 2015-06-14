#include "State.h"

//Constructors
State::State(int state_label, Configuration init_config, float rew): 
label(state_label), block_configuration(init_config), reward(rew){prev_action = NULL;}
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
	vector<Block> state_actionable_blocks;
	vector<Block>::iterator it;
	int i = 0;
	float Q_val;
	float trans_prob;
	for(it = block_configuration.getActionableBlockArray()->begin(); it != block_configuration.getActionableBlockArray()->end(); it++){
		state_actionable_blocks.push_back(*it);
	}
	if(prev_action == NULL || prev_action->getAction() == PUT_DOWN){
		for(it=state_actionable_blocks.begin(); it!=state_actionable_blocks.end(); it++){
			Q_val = prevQValues();
			trans_prob = calcTransitionProbability();
			actions.push_back(State_Action(i, Q_val, trans_prob, *it, PICK_UP));
			i++;
		}
	}else if(prev_action->getAction() == PICK_UP){
		Q_val = prevQValues();
		trans_prob = calcTransitionProbability();
		actions.push_back(State_Action(i, Q_val, trans_prob, prev_action->getActionBlock(), PUT_DOWN));
		i++;
		for(it=state_actionable_blocks.begin(); it!=state_actionable_blocks.end(); it++){
			Q_val = prevQValues();
			trans_prob = calcTransitionProbability();
			actions.push_back(State_Action(i, Q_val, trans_prob, prev_action->getActionBlock(), PUT_DOWN, &(*it)));
			i++;
		}
	}
}
