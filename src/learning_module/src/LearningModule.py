# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 12:16:58 2015

@author: Prashanth
"""

"""This is a Service Node. Any requests will be responded with outputs."""

""" Onpolicy requests will be responded with a boolean (success/ failure)"""

from MDP import MDP
from Block import Block
from State import State
from copy import deepcopy
from collections import OrderedDict
from scipy import stats
from scipy.cluster.vq import vq, kmeans, whiten
import numpy
import operator
from DecisionTree import *

from asp_module.msg import State as StateMsg
from asp_module.msg import Configuration as ConfigMsg
from asp_module.msg import Block as BlockMsg
class LearningModule:
    def __init__(self):
        self.mdp_list = []
        self.error_config = []
        self.success_config = []
        self.decision_tree = None
        
        src_error = rospy.Service('LMErrorHasOccured',LMErrorHasOccured, self.errorHandle)
        src_rules = rospy.Service('LMGenerateRules', LMGenerateRules, self.generateRules)
        srv_state = rospy.Service('LMCurrentState', LMCurrentState, self.initialise_mdp)
        srv_action = rospy.Service('LMStateActionTaken', LMStateActionTaken, self.onPolicyLearning)

    def initialise_lists(self):
        self.mdp_list.append([])
        self.error_config.append([])
        self.success_config.append([])

    def initialise_mdp(self):
        blocks = []
        for prop in StateMsg.block_properties:
            block.append(Block(prop.label, prop.shape, prop.colour))
        start_config = StateMsg.configuration
        initialise_lists()
        self.success_config[-1].append(start_config)
        label = len(self.mdp_list[-1])
        mdp = MDP(label, blocks)
        startingState = State(0, start_config)
        mdp.statelist.append(startingState)
        mdp.initMDP(startingState)
        self.mdp_list[-1].append(mdp)

    def combineIdenticalMDPs(self, mdp_list):
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

    def findState(self, config, mdp):
        for state in mdp.getStateList():
            if state.getConfiguration() == config:
                return state

    def errorHandle(self, action_chosen):
        action_block = action_chosen.actionableBlock
        dest_block = action_chosen.destinationBlock
        for action in self.mdp_list[-1][-1].getErrorState().getActions():
            if action.getActionableBlock() == int(action_block[1:]):
                if action.getDestinationBlock() == int(dest_block[1:]):
                    action_chosen = action
        self.mdp_list[-1][-1].onPolicyLearning(action_chosen)
        error_config = self.mdp_list.getErrorState().getConfiguration()
        self.errorconfig[-1].append(error_config)
        self.mdp_list[-1][-1].simulation(errorconfig, self.success_config[-1])
        return 0

    def onPolicyLearning():
        """ This will be the callback function"""
        #action_chosen = getFromMessage
        self.mdp_list[-1][-1].onPolicyLearning(action_chosen)
        config = self.mdp_list[-1][-1].getErrorState().getConfig
        self.success_config[-1].append(config)
        """ Get the message and parse it to be passed into the function"""

    def writeToList(self, mdp_list, training_set = None):
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
                                   blocks[action_block].getColour(),blocks[action_block].getSize(), blocks[dest_block].getShape(),
                                   blocks[dest_block].getColour(),blocks[dest_block].getSize(),
                                   mdp.getQMatrix()[state.getLabel()][action.getNextStateAddr()])
                    training_set.append(example)
        return training_set

    def generateRules(self, training_set):
        reduced_mdp_list = []
        attributes = []
        for mdps in self.mdp_list:
            reduced_mdp = self.combineIdenticalMDPs(mdps)
            reduced_mdp_list.append(reduced_mdp)

        attr_shape = ("Prism", "Cube", "Cuboid")
        attr_colour = ("Red", "Blue", "Green")
        attr_size = ("Small","Medium","Large")
        attribute_dict = [("has_shape(A,", attr_shape), ("has_colour(A, ", attr_colour), ("has_size(A, ", attr_size),
                            ("has_shape(D, ", attr_shape), ("has_colour(D, ",attr_colour), ("has_size(D, )", attr_size)]
        attribute_dict = OrderedDict(attribute_dict)
        index = 0
        names = attribute_dict.keys()
        values = attribute_dict.values()
        for name, vals in zip(names, values):
            attributes.append(Attribute(name, index, vals))
            index += 1
        self.decision_tree = DecisionTree(attributes, training_set)
        rules = decision_tree.createDecisionTree()
        rules = selectRules(rules)
        return rules

    def selectRules(self, rules):
        """ Select the best rules """
        """ Think about doing it using SVM"""
        rules = sorted(rules, key=operator.itemgetter(-1))
        q_val = []
        for index, rule in enumerate(rules):
            q_val.append([index, rule[-1]])
        whitened = whiten(q_val)
        centroids,_ = kmeans(whitened, 3, thresh = 1,iter = 100)
        ids,_= vq(whitened, centroids)
        key = ids[-1]
        indices = []
        for index, keys in enumerate(ids):
            if key == keys:
                indices.append(index)
        valid_rules = []
        for index in indices:
            valid_rules.append(rules[index][0])
        return self.parseRules(valid_rules)

    def parseRules(self, rules):
        valid_rules = []
        for rule in rules:
            sentence = ""
            for segment in rule:
                sentence = sentence + segment + ", "
            sentence = sentence[:-2]
            valid_rules.append(sentence)
        return Rules(generatedRules = valid_rules)

    def reduceMDP(self,errorconfig, stack_config, start_config, blocks):
        mdp_list = []
        for i in range(0, len(errorconfig)):
            mdp_list.append(MDP(i, blocks))
            startingState = State(0, start_config)
            mdp_list[i].statelist.append(startingState)
            mdp_list[i].initMDP(startingState)
            errorstate = self.findState(errorconfig[i], mdp_list[i])
            stackstate = []
            for j in range(0,len(stack_config)):
                stackstate.append(self.findState(stack_config[j], mdp_list[i]))
            mdp_list[i].simulation(errorstate, stackstate)
            mdp_list[i].updateDistanceMatrix(errorstate)

        reduced_mdp = self.combineIdenticalMDPs(mdp_list)
        return reduced_mdp




def main():
    """The blocks"""

    learning_module = LearningModule()

    blocks = []
    blocks.append(Block(0, "Prism", "Red", "Small"))
    blocks.append(Block(1, "Cube", "Red", "Small"))
    blocks.append(Block(2, "Cuboid", "Red", "Small"))
    blocks.append(Block(3, "Cube", "Red", "Large"))

    """
    Starting Config (Can be any configuration.
    Ideally should be the starting configuration of the blocks in the real world
    """
    config = [-1,-1,-1,-1]
    mdp_list = []

    """Colour"""
#    errorconfig = [[-1,0,-1],[-1,2,-1],[1,-1,-1],[-1,-1,1],[-1,0,1],[1,2,-1],[1,-1,0],[2,-1,1]]
#    stack_config = [[-1,-1,-1],[-1,-1,0],[2,-1,-1]]
    """Shape"""
    errorconfig = [[-1,0,-1,-1],[-1,-1,0,-1],[1,-1,0,-1],[2,0,-1,-1],[-1,-1,-1,0],[-1,-1,-1,1],[-1,-1,-1,2]]
    stack_config = [[-1,-1,-1,-1],[1,-1,-1,-1],[2,-1,-1,-1],[-1,2,-1,-1],[1,2,-1,-1]]

    """Create a new MDP"""

    mdp1 = learning_module.reduceMDP(errorconfig, stack_config, config, blocks)

    blocks = []
    blocks.append(Block(0, "Prism", "Blue", "Medium"))
    blocks.append(Block(1, "Cube", "Blue", "Medium"))
    blocks.append(Block(2, "Cuboid", "Blue", "Medium"))
    blocks.append(Block(3, "Cube", "BLue", "Large"))

    mdp_list = []
    """Colour"""
#    errorconfig = [[-1,0,-1],[-1,-1,0],[1,-1,-1],[2,-1,-1],[1,-1,0],[2,0,-1],[-1,0,1],[-1,2,0]]
#    stack_config = [[-1,-1,-1],[-1,2,-1],[-1,-1,1]]
    """Shape"""
    errorconfig = [[-1,0,-1,-1],[-1,-1,0,-1],[1,-1,0,-1],[2,0,-1,-1],[-1,-1,-1,0],[-1,-1,-1,1],[-1,-1,-1,2]]
    stack_config = [[-1,-1,-1,-1],[1,-1,-1,-1],[2,-1,-1,-1],[-1,2,-1,-1],[1,2,-1,-1]]


    mdp2 = learning_module.reduceMDP(errorconfig, stack_config, config, blocks)

    blocks = []
    blocks.append(Block(0, "Prism", "Green", "Large"))
    blocks.append(Block(1, "Cube", "Green", "Large"))
    blocks.append(Block(2, "Cuboid", "Green", "Large"))
    blocks.append(Block(3, "Cube", "Red", "Large"))

    mdp_list = []
    """Colour"""
#    errorconfig = [[-1,-1,0],[-1,-1,1],[2,-1,-1],[-1,2,-1],[1,2,-1],[2,-1,1],[-1,2,0],[1,-1,0]]
#    stack_config = [[-1,-1,-1],[-1,0,-1],[1,-1,-1]]
    """Shape"""
    errorconfig = [[-1,0,-1,-1],[-1,-1,0,-1],[1,-1,0,-1],[2,0,-1,-1],[-1,-1,-1,0],[-1,-1,-1,1],[-1,-1,-1,2]]
    stack_config = [[-1,-1,-1,-1],[1,-1,-1,-1],[2,-1,-1,-1],[-1,2,-1,-1],[1,2,-1,-1]]

    mdp3 = learning_module.reduceMDP(errorconfig, stack_config, config, blocks)

    blocks = []
    blocks.append(Block(0, "Prism", "Green", "Small"))
    blocks.append(Block(1, "Cube", "Green", "Small"))
    blocks.append(Block(2, "Cuboid", "Green", "Small"))
    blocks.append(Block(3, "Cube", "Green", "Large"))

    mdp_list = []
    """Colour"""
#    errorconfig = [[-1,-1,0],[-1,-1,1],[2,-1,-1],[-1,2,-1],[1,2,-1],[2,-1,1],[-1,2,0],[1,-1,0]]
#    stack_config = [[-1,-1,-1],[-1,0,-1],[1,-1,-1]]
    """Shape"""
    errorconfig = [[-1,0,-1,-1],[-1,-1,0,-1],[1,-1,0,-1],[2,0,-1,-1],[-1,-1,-1,0],[-1,-1,-1,1],[-1,-1,-1,2]]
    stack_config = [[-1,-1,-1,-1],[1,-1,-1,-1],[2,-1,-1,-1],[-1,2,-1,-1],[1,2,-1,-1]]

    mdp4 = learning_module.reduceMDP(errorconfig, stack_config, config, blocks)


    mdp_list = [mdp1, mdp2, mdp3, mdp4]
    training_set = learning_module.writeToList(mdp_list)

    attr_shape = ("Prism", "Cube", "Cuboid")
    attr_colour = ("Red", "Blue", "Green")
    attr_size = ("Small","Medium","Large")
    attribute_dict = [("has_shape(A,", attr_shape), ("has_colour(A, ", attr_colour), ("has_size(A, ", attr_size),
                        ("has_shape(D, ", attr_shape), ("has_colour(D, ",attr_colour), ("has_size(D, ", attr_size)]

    attribute_dict = OrderedDict(attribute_dict)
    attributes = []
    index = 0
    names = attribute_dict.keys()
    values = attribute_dict.values()
    for name, vals in zip(names, values):
        attributes.append(Attribute(name, index, vals))
        index += 1
    decision_tree = DecisionTree(attributes, training_set)
    #print training_set
    rules = decision_tree.getRules()
    learning_module.selectRules(rules)
