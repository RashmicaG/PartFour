#ifndef STATE_ACTION_H
#define STATE_ACTION_H
#include <iostream>
#include <stddef.h>
#include <vector>
#include <stdlib.h>
using namespace std;

enum Destination{DEST_ON_TABLE, DEST_ON_ARM, DEST_ON_BLOCK};
enum Action{PICK_UP, PUT_DOWN};
class State_Action{
	int label;
	float Q_value;
	float transition_probablity;
	Block actionable_block;
	Action action;
	Destination destination;
	Block* destination_block;
	public:
		// Constructor
		State_Action(int, float, float, Block, Action);
		State_Action(int, float, float, Block, Action, Block*);
		
		// Destructor
		~State_Action(void){}
		
		// Getters
		int getLabel(){return label;}
		float getQValue(){return Q_value;}
		float getTransitionProbablity(){return transition_probablity;}
		Block getActionableBlock(){return actionable_block;}
		Action getAction(){return action;}

		// Setters
		void setQValue(float value){ Q_value = value;}
		void setTransitionProbablity(float tp_value){transition_probablity = tp_value;}
};
#endif
