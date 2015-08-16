# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 12:16:58 2015

@author: Prashanth
"""
from MDP import MDP
from Block import Block
from State import State
from copy import deepcopy
from collections import OrderedDict
from DecisionTree import *
import csv
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
    
    newMDP = deepcopy(mdp_list[0])
    newMDP.setQMatrix(weighted_average)
    return newMDP
    
def findState(config, mdp):
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
                    example = (blocks[action_block].getShape(), blocks[action_block].getColour(), 
                               mdp.getQMatrix()[state.getLabel()][action.getNextStateAddr()])
                else:
                    example = (blocks[action_block].getShape(), 
                               blocks[action_block].getColour(),blocks[dest_block].getShape(), 
                               blocks[dest_block].getColour(),
                               mdp.getQMatrix()[state.getLabel()][action.getNextStateAddr()])
                training_set.append(example)
    return training_set

def main():
    """The blocks"""
    blocks = []
    blocks.append(Block(0, "Cube", "Red"))
    blocks.append(Block(1, "Cube", "Blue"))
    blocks.append(Block(2, "Cube", "Red"))
    
    """ 
    Starting Config (Can be any configuration. 
    Ideally should be the starting configuration of the blocks in the real world
    """
    config = [-1,-1,-1]
    startingState = State(0, config)
    mdp_list = []
    errorconfig = [[-1,0,-1],[-1,2,-1],[-1,0,1],[1,2,-1]]
    stack_config = [[-1,-1,-1], [2,-1,-1]]
    """Create A new MDP"""
    for i in range(0,len(errorconfig)):
        mdp_list.append(MDP(i, blocks))
        startingState = State(0, config)
        mdp_list[i].statelist.append(startingState)
        mdp_list[i].initMDP(startingState)
        errorstate = findState(errorconfig[i], mdp_list[i])
        stackstate = []
        for j in range(0,len(stack_config)):
            stackstate.append(findState(stack_config[j], mdp_list[i]))
        mdp_list[i].simulation(errorstate, stackstate)
        mdp_list[i].updateDistanceMatrix(errorstate)
    
    mdp1 = combineIdenticalMDPs(mdp_list)
    
    blocks = []
    blocks.append(Block(0, "Cuboid", "Blue"))
    blocks.append(Block(1, "Cuboid", "Red"))
    blocks.append(Block(2, "Cuboid", "Blue"))
    mdp_list = []
    errorconfig = [[1,-1,0],[-1,0,-1],[-1,-1,0],[2,0,-1],[1,-1,-1],[-1,2,-1],[1,2,-1]]
    stack_config = [[-1,-1,-1], [2,-1,-1]]
    for i in range(0,len(errorconfig)):
        mdp_list.append(MDP(i, blocks))
        startingState = State(0, config)
        mdp_list[i].statelist.append(startingState)
        mdp_list[i].initMDP(startingState)
        errorstate = findState(errorconfig[i], mdp_list[i])
        stackstate = []
        for j in range(0,len(stack_config)):
            stackstate.append(findState(stack_config[j], mdp_list[i]))
        mdp_list[i].simulation(errorstate, stackstate)
        mdp_list[i].updateDistanceMatrix(errorstate)
    
    mdp2 = combineIdenticalMDPs(mdp_list)
    
    blocks = []
    blocks.append(Block(0, "Prism", "Yellow"))
    blocks.append(Block(1, "Cube", "Yellow"))
    blocks.append(Block(2, "Cuboid", "Yellow"))
    mdp_list = []
    errorconfig = [[1,-1,0],[-1,0,-1],[-1,-1,0],[2,0,-1]]
    stack_config = [[-1,-1,-1], [2,-1,-1],[1,-1,-1],[-1,2,-1],[1,2,-1]]    
    for i in range(0,len(errorconfig)):
        mdp_list.append(MDP(i, blocks))
        startingState = State(0, config)
        mdp_list[i].statelist.append(startingState)
        mdp_list[i].initMDP(startingState)
        errorstate = findState(errorconfig[i], mdp_list[i])
        stackstate = []
        for j in range(0,len(stack_config)):
            stackstate.append(findState(stack_config[j], mdp_list[i]))
        mdp_list[i].simulation(errorstate, stackstate)
        mdp_list[i].updateDistanceMatrix(errorstate)
    
    mdp3 = combineIdenticalMDPs(mdp_list)
    
    
    mdp_list = [mdp1, mdp2]#, mdp3]
    training_set = writeToList(mdp_list)

    attribute_dict = [("has_shape(A,", ("Prism", "Cube", "Cuboid")), ("has_colour(A, ",("Red","Blue","Yellow")), ("has_shape(D, ", ("Prism", "Cube", "Cuboid")), ("has_colour(D, ",("Red","Blue","Yellow"))]
    attribute_dict = OrderedDict(attribute_dict)
    #rand_smpl = [ training_set[i] for i in sorted(random.sample(xrange(len(training_set)), len(training_set)/2))]
    attributes = []
    index = 0
    names = attribute_dict.keys()
    values = attribute_dict.values()
    for name, vals in zip(names, values):
        attributes.append(Attribute(name, index, vals))
        index += 1
    decision_tree = DecisionTree(attributes, training_set)
    #print training_set
    tree = decision_tree.createDecisionTree()
    #q_values = open('MDP_Data.csv', 'w')
    
    
        
    

main()
