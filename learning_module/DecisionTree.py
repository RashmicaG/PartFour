# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:06:48 2015

@author: Prashanth
"""

"""
Node is either an attribute or a leaf. 
A node would contain its own subset. This it receives from the parent node and 
branch it came from.
A node contains its children nodes.
A node contains its own set of information.
It needs to be seperated 
"""
from copy import deepcopy
class Node:
    def __init__(self, attribute, training_set):
        self.attribute = attribute
        self.children_nodes = []
        self.children_attr = []
        self.rules = []
        self.training_set = training_set
        self.leaf = False
        self.bound = 0.0
    def isLeafNode(self):
        if self.attribute == None:
            return True
        elif self.leaf == True:
            return True
        else:
            return False
    def setLeafNode(self):
        self.leaf = True
    
    def setChildrenAttributes(self, children_attr):
        self.children_attr = children_attr
    def getChildrenAttributes(self):
        return self.children_attr    
    
    
    
    def setRules(self, rules):
        self.rules = rules
    def getRules(self):
        return self.rules
        
    def getAttribute(self):
        return self.attribute
    def getBound(self):
        return self.bound
    def setBound(self, bound):
        self.bound = bound
    def addChildNode(self, child):
        self.children_nodes.append(child)
    def getTrainingSet(self):
        return self.training_set
    def getChildren(self):
        return self.children_nodes
    
class Attribute:
    def __init__(self, name, index, values):
        self.name = name
        self.index = index
        self.values = values
    def getName(self):
        return self.name
    def getIndex(self):
        return self.index
    def getValues(self):
        return self.values

class DecisionTree:
    def __init__(self, attributes, training_sample, test_sample = None):
        self.parent_node = None
        self.attributes = attributes
        self.training_sample = training_sample
        self.test_sample = test_sample
        self.bound = float("inf") 
    def createDecisionTree(self, current_node = None):
        stack = []
        if current_node == None:
            current_node = self.findNextBestNode(self.attributes, self.training_sample)
        stack.append(current_node)
        position = self.findPositionOfAttribute(self.attributes, current_node)
        other_attr = self.attributes[:position] + self.attributes[position+1:]
        self.parent_node = current_node
        subsets = self.createSubsets(current_node)
        subsets = self.prioritizeSubsets(subsets)
        if len(subsets) > 1:
            for subset in subsets:
                child_node = self.findNextBestNode(other_attr, subset[1])
                if child_node != None:
                    child_node.setBound(subset[-1])
                    new_rule = current_node.getRules()+[(current_node.getAttribute().getName()+subset[0]+")")]
                    child_node.setRules(new_rule)
                    position = self.findPositionOfAttribute(other_attr, child_node)
                    child_attrs = other_attr[:position] + other_attr[position+1:]
                    child_node.setChildrenAttributes(child_attrs)
                    stack.append(child_node)
                    current_node.addChildNode(child_node)        
        
        current_node.setChildrenAttributes(other_attr)
        stack.remove(current_node)
        stack_pointer = len(stack)-1
        bound = current_node.getBound()
        while(len(stack)>0):
            current_node = stack[stack_pointer]            
            if len(current_node.getChildrenAttributes()) == 0:
                last_attr = current_node.getTrainingSet()[0][current_node.getAttribute().getIndex()]
                new_rule = current_node.getRules()+[(current_node.getAttribute().getName()+ last_attr +")")]
                child_node = Node(None, subsets[-1])
                current_node.addChildNode(child_node)
                child_node.setRules(new_rule)
                print (current_node.getChildren()[-1].getRules(), current_node.getTrainingSet()[0]);
                stack.remove(current_node)
                stack_pointer = len(stack)-1            
            elif stack_pointer < 0:
                for node in stack:
                    node.setLeafNode()
                    print (node.getRules(), node.getTrainingSet()[0])
                break;
            elif current_node.getBound() > bound:
                subsets = self.createSubsets(current_node)
                subsets = self.prioritizeSubsets(subsets)
                if len(subsets) > 1:
                    other_attr = deepcopy(current_node.getChildrenAttributes())
                    if len(other_attr)>0:
                        for subset in subsets:
                            child_node = self.findNextBestNode(other_attr, subset[1])
                            new_rule = current_node.getRules()+[(current_node.getAttribute().getName()+subset[0]+")")]
                            if child_node != None:
                                child_node.setBound(subset[-1])
                                position = self.findPositionOfAttribute(other_attr, child_node)
                                child_attrs = other_attr[:position] + other_attr[position+1:]
                                child_node.setChildrenAttributes(child_attrs)
                                stack.append(child_node)
                                current_node.addChildNode(child_node)
                                child_node.setRules(new_rule)

                stack.remove(current_node)
                stack_pointer = len(stack) - 1
            elif current_node.getBound() <= bound:
                stack_pointer -= 1
                bound = current_node.getBound()
        return self.parent_node
    
    def findPositionOfAttribute(self, attributes, node):
        i = 0
        for attr in attributes:
            if node.getAttribute().getName() == attr.getName():
                return i
            i+=1
        print "Not Found"
        return None
    
    def prioritizeSubsets(self, subsets):
        subsets.sort(key=lambda x: x[2])        
        return subsets
    def getParentNode(self):
        return self.parent_node
                    
    def calcVariance(self, qlist):
        average = float(sum(qlist))/float(len(qlist))
        variance = 0.0
        for qval in qlist:
            variance += (average - qval)**2
        return variance
            
    def createSubsets(self, current_node):
        temp_subsets = []
        subsets = []
        for value in current_node.getAttribute().getValues():
            temp_subsets.append([value, [], 0.0])
        for example in current_node.getTrainingSet():
            for value in temp_subsets:
                if len(example) > 3:
                    if example[current_node.getAttribute().getIndex()] == value[0]:
                        value[1].append(example)
        for value in temp_subsets:
            if len(value[1]) > 0:
                subsets.append(value)
        for value in subsets:
            qlist = []
            for example in value[1]:
                qlist.append(example[-1])
            variance = self.calcVariance(qlist)
            value[2] = variance
        return subsets
        
    def findNextBestNode(self, attributes, training_sample):
        current_best = None
        variance_min = float("inf")
        qlist = []
        for sample in training_sample:
			qlist.append(sample[-1])
        original_var = self.calcVariance(qlist)
        for attr in attributes:
            temp_node = Node(attr, training_sample)
            temp_subsets = self.createSubsets(temp_node)
            temp_max = 0.0
            info_gain = 0.0
            for each in temp_subsets:
				temp_max += each[-1]
            info_gain = original_var - temp_max
            if variance_min > info_gain:
                current_best = temp_node
                variance_min = info_gain
        if current_best != None:
            current_best.setBound(variance_min)
        return current_best
        """
        for a given set of attributes:
            i will create subsets
            check the max variance of each subset
            choose the attribute which gives min variance
            return the node
        
        """
