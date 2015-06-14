#include "Q-Learning.h"

class MDP{
	//State initial_state;
	public:
	MDP(){
		vector<Block> block_vector(1, Block(1, STATUS_ON_TABLE, CUBOID, MEDIUM, RED));
		block_vector.push_back(Block(2, STATUS_ON_TABLE, CUBOID, SMALL, BLUE));
		block_vector.push_back(Block(3, STATUS_ON_TABLE, PRISM, LARGE, GREEN));
		block_vector.push_back(Block(4, STATUS_ON_TABLE, CUBE, SMALL, RED));
		vector<State_Action> action;
		vector<State> states;
		Configuration config(&block_vector);
		
		State initstate(0, config, 2);
		initstate.createStateActions();
		vector<State_Action>:: iterator it;
		for (it=initstate.getStateActions()->begin(); it!=initstate.getStateActions()->end(); it++){
			if(it->getAction() == PICK_UP){
				cout << "PICK_UP block " << it->getActionBlock().getLabel() << endl;
			}else{
				if(it->getDestinationBlock() != NULL)
					cout << "PUT_DOWN block " << it->getActionBlock().getLabel()<< "on "<< it->getDestinationBlock()->getLabel() << endl;
				else{
					cout << "PUT_DOWN block " << it->getActionBlock().getLabel()<< "on "<< "table"<< endl;
				}
			}
		}
		//State nextstate1(1, config, 2, &action.at(0));
		//states.push_back(nextstate1);
		//initstate.setNextStates(&states);
		//cout << initstate.getNextState().back().getLabel() << endl;
	}
	
	void Q_Learning(State);
};

void MDP::Q_Learning(State currentState){
	
}
int main (){
  new MDP();
}
