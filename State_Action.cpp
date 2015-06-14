#include "State_Action.h"
State_Action::State_Action(int action_label, float Q_val, float trans_prob, Block block, Action act): 
label(action_label), Q_value(Q_val), transition_probablity(trans_prob), actionable_block(block), action(act){ destination_block = NULL;}
State_Action::State_Action(int action_label, float Q_val, float trans_prob, Block block, Action act, Block* dest_block): 
label(action_label), Q_value(Q_val), transition_probablity(trans_prob), actionable_block(block), action(act), destination_block(dest_block){}
