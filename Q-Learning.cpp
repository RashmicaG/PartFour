#include "Q-Learning.h"

class MDP{
	//State initial_state;
	public:
	MDP(){
		//vector<Block> block_vector(1, Block(1, ON_TABLE, CUBOID, MEDIUM, RED));
		//block_vector.push_back(Block(2, ON_TABLE, CUBOID, SMALL, BLUE));
		//block_vector.push_back(Block(3, ON_TABLE, PRISM, LARGE, GREEN));
		//block_vector.push_back(Block(4, ON_TABLE, CUBE, SMALL, RED));
		//vector<State_Action> action;
		//vector<State> states;
		//Configuration config(block_vector.size(), &block_vector);
		
		//int i=0;
		//vector<Block>::iterator it;
		//for (it = block_vector.begin(); it != block_vector.end(); it++){
			//float Q_val = 1.5;
			//float trans_prob = 0.25;
			//Action act = Action((bool)rand%2);
			//action.push_back(State_Action(i, Q_val, trans_prob, *it, act));
			//i++;
		//}
		//State initstate(0, config, &action, 2, action.size());
		//State nextstate1(1, config, &action, 2, action.size(), &action.at(0));
		//states.push_back(nextstate1);
		//initstate.setNextStates(&states);
		//cout << initstate.getNextState().front().getLabel() << endl;
	}
	
	void Q_Learning(State);
};

void MDP::Q_Learning(State currentState){
	
}
int main (){
  new MDP();
}
