#!/usr/bin/env python

import rospy
from asp_module.srv import *
from asp_module.msg import *
from std_msgs.msg import Int16
from collections import deque
import random
import types

class Robot:
    def __init__(self):
        self.timestep = 1
        self.goalActive = False
        self.nextAction = 'null'
        self.goalQueue = [] # how to initialise queue.?
        self.goalState
        self.currentState


    def sendGoal(self):
        """" This is the start of each iteration. Should we update timestep here?
        hmmmmm"""
        try:
            # If nothing in goalQueue then generate random goal
            if not self.goalQueue:
                self.getAnswerSet(self.generateGoal())
            else:
                self.getAnswerSet(self.goalQueue.popleft())
        except:
            print "sendGoal failed"

    def generateBlockConfig(self, max = 5, min = 3 ):
         """ A configuration of blocks is represented as 
        a list. Each index represents a block, and the value 
        at this index represents what this block is on:
        -1 - table, 0-n: the index of the block it is on.
        MAX and MIN CANNOT be the same"""

        # check values of max and min
        if not (type(max) == type(min) and type(max) == types.IntType):
            print "Max or Min is not an int. Using default of 3 or 4 blocks"
            min = 3
            max = 5

        if min < 0:
            print 'min must be larger than zero. Setting to 0.'
            min = 0

        if max < 0:
            print 'max must be larger than zero. Setting to 1.'
            max = 1

        if max <= min:
            print 'max must be BIGGER than min. Increasing max.'
            max = min + 1

        # make sure a block cannot be on itself
        size = random.randrange(min, max)
        config = [-1]* size

        index = -1
        for block in config:
            index = index+1
            is_on = random.randrange(-1, size+1)
            while( (is_on in config and is_on != -1) or (is_on == index) ):
                # while this value has been used and isn't -1
                # or while this value is not the block itself
                is_on = random.randrange(-1, size+1)
                
            config[index] = is_on
        print config

        self.goalConfig = config

    def generateGoal(self):
       generateBlockConfig() 
       # send this to controller
       

    def sendGoalToAspModule(self):
        pass

    def sendGoalTo



    def getAnswerSet(self, data):
        """ This sends goal to asp_module and returns back action.
        If we want next action we just send same goal. """
        rospy.wait_for_service('AspAnswer')
        try:
            asp_answer = rospy.ServiceProxy('AspAnswer', AspAnswer)
            self.nextAction = asp_answer(data)

            print self.nextAction

            self.goalActive = True
            # return ans_response

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

    def publisher(self, pub, msg):
        try:
            pub.publish(msg)
        except:
            print "Publishing failed call failed:"

        return
            

    def executeAction(self, action):
        """ This will send action to robot module and return feedback"""
        pass

    def getConfigBlocks(self):
        """ Gets configuration of blocks from robot"""
        pass




if __name__ == '__main__':
    rospy.init_node('controller', anonymous=True)
    r = Robot()



    
    timestep_publisher = rospy.Publisher('/controller/timestep', Int16, queue_size=10)
    
    observation_publisher = rospy.Publisher('/controller/observations', Observation, queue_size=10)  
    # configuration_publisher = rospy.Publisher('/controller/configuration', Configuration, queue_size=10)    
     # rate = rospy.Rate(10)
    print 'Publishers running...'
    
    r.generateGoal()


    r.getAnswerSet('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    r.getAnswerSet('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    r.publisher( timestep_publisher, r.timestep)
    r.getAnswerSet('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    
    # holds(on(block1, s2), 0).
    obs = (Observation(negation=False, fluent='on', argument1='block1', argument2='s2', timestep=r.timestep))
    print
    print 'obs sent :'
    print obs
    r.publisher(observation_publisher, obs)

    # while not rospy.is_shutdown():
        # rate.sleep()
