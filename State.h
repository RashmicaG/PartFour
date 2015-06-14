#ifndef STATE_H
#define STATE_H
#include <stddef.h>
#include <vector>
#include <stdlib.h>
#include "Block.h"
#include "Configuration.h"
#include "State_Action.h"
#include "Constants.h"
using namespace std;

class State{
	int label;
	Configuration block_configuration;
	float reward;
	State_Action* prev_action;
	vector<State_Action> actions;
	vector<State> next_states;
	public:
		//Constructors
		State();
		State(int, Configuration, float); // Initial State
		State(int, Configuration, float, State_Action*); // State after a transition
		//getter
		int getLabel(){return label;}
		Configuration getBlockConfiguration(){return block_configuration;}
		float getReward(){return reward;}
		vector<State_Action>* getStateActions(){return &actions;}
		vector<State> getNextState(){return next_states;}
		//Destructor
		~State(void){};
		//setter
		void setReward(float r){reward = r;}
		void setNextStates(vector<State>*);
		
		//Methods
		void createStateActions();
		float prevQValues();
		float calcTransitionProbability();
};
#endif
