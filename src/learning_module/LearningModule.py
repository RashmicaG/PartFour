# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 12:16:58 2015

@author: Prashanth
"""
from MDP import MDP
from Block import Block
from State import State
from copy import deepcopy

def combineIdenticalMDPs(mdp_list):
    sum_distance = [[0.0 for i in range(0,len(mdp_list[0].getStateList()))] for i in range(0,len(mdp_list[0].getStateList()))]
    weighted_average = [[0.0 for i in range(0,len(mdp_list[0].getStateList()))] for i in range(0,len(mdp_list[0].getStateList()))]
    for mdp in mdp_list:
        for i, row in enumerate(mdp.getDistanceMatrix()):
            for j, distance in enumerate(row):
                if distance > 0:
                    sum_distance[i][j] += 1/distance
    for mdp in mdp_list:
        for i, row in enumerate(mdp.getDistanceMatrix()):
            for j, distance in enumerate(row):
                if distance > 0.0 and sum_distance[i][j] > 0.0:
                    weight = (1/distance)/(sum_distance[i][j])
                    weighted_average[i][j] += weight*mdp.getQMatrix()[i][j]
                    print (i,j,weighted_average[i][j])
    
    newMDP = deepcopy(mdp_list[0])

    newMDP.setQMatrix(weighted_average)
    print weighted_average[2][11]
    print "\n"
    return newMDP
    
def findErrorState(config, mdp):
    for state in mdp.getStateList():
        if state.getConfiguration() == config:
            return state

def writeToList(mdp_list, training_set = None):
    if training_set == None:
        training_set = []
    for mdp in mdp_list:
        blocks = mdp.getBlocks()
        for state in mdp.getStateList():
            for action in state.getActions():
                action_block = action.getActionableBlock()
                dest_block = action.getDestinationBlock()
                if dest_block == None:
                    example = (state.getConfiguration(), blocks[action_block].getShape(), 
                               blocks[action_block].getSize(), blocks[action_block].getColour(), 
                               mdp.getQMatrix()[state.getLabel()][action.getNextStateAddr()])
                else:
                    example = (state.getConfiguration(), blocks[action_block].getShape(), 
                               blocks[action_block].getSize(), blocks[action_block].getColour(),
                               blocks[dest_block].getShape(), 
                               blocks[dest_block].getSize(), blocks[dest_block].getColour(),
                               mdp.getQMatrix()[state.getLabel()][action.getNextStateAddr()])
                training_set.append(example)
    return training_set

def main():
    """The blocks"""
    blocks = []
    blocks.append(Block(0, "Prism", "Small", "Red"))
    blocks.append(Block(1, "Cube", "Small", "Red"))
    blocks.append(Block(2, "Cuboid", "Small", "Red"))
    """ 
    Starting Config (Can be any configuration. 
    Ideally should be the starting configuration of the blocks in the real world
    """
    config = [-1,-1,-1]
    startingState = State(0, config)
    
    """Create A new MDP"""
    mdp1 = MDP(0, blocks)
    mdp1.statelist.append(startingState)
    mdp1.initMDP(startingState)
    """Create an error state. Configuration should come from the robot."""
    errorconfig = [2,-1,-1]
    errorstate = findErrorState(errorconfig, mdp1)
    error_action = None
    for action in errorstate.getActions():
        if action.getActionableBlock() == 1 and action.getDestinationBlock() == 0:
            error_action = action
            break
    """Do simulation"""
    mdp1.simulation(errorstate, error_action)
    """Updates the distance matrix. The distance distance is from """
    mdp1.updateDistanceMatrix(errorstate, error_action)
   
    startingState = State(0, config)

    """Create A new MDP"""
    mdp2 = MDP(0, blocks)
    mdp2.statelist.append(startingState)
    mdp2.initMDP(startingState)
    """Create an error state. Configuration should come from the robot."""
    errorconfig = [1,-1,-1]
    errorstate = findErrorState(errorconfig, mdp2)
    error_action = None
    for action in errorstate.getActions():
        if action.getActionableBlock() == 2 and action.getDestinationBlock() == 0:
            error_action = action
            break
    mdp2.simulation(errorstate, error_action)
    """Updates the distance matrix. The distance distance is from """    
    mdp2.updateDistanceMatrix(errorstate, error_action)    
    
    
    mdp_list = [mdp1,mdp2]
    newMDP = combineIdenticalMDPs(mdp_list)
    mdp_list = [newMDP]
    training_set = writeToList(mdp_list)
    for train in training_set:
        print train
main()