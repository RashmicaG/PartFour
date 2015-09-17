#!/usr/bin/env python

import rospy
from asp_module.srv import *
from asp_module.msg import *
from asp_module import *
from learning_module import *
from std_msgs.msg import Int16
from collections import deque
from learning_module.msg import *
from learning_module.srv import *
from copy import deepcopy
import random
import types
import os
import re


class Robot:
    def __init__(self):
        self.state = 'initial'
        self.timestep = 1
        self.goalActive = False
        self.goalConfig = Configuration([])
        self.currentState = State(Configuration([]), [] )
        self.currentAction = Action('null', 'null', 'null', 0, Configuration([]),  False)
        self.newSet = True
        self.dict = {}
        self.prevGoalConfig = Configuration([])

        # self.blocks = [Block('null', 'null', 'null', 'null'), Block('null', 'null', 'null', 'null')]
                # only for testing purposes
        self.blocks = [Block('block0', 'cuboid', 'blue', 'small'), 
                    Block('block1', 'prism', 'red', 'small'), 
                    Block('block2', 'cube', 'blue', 'small'), 
                    # Block('block3', 'cube', 'red', 'small'),
                    # Block('block4', 'prism', 'small', 'yellow')
                    ]

        self.rules = Rules([])

        rospy.init_node('controller', anonymous=True)
        srv_state = rospy.Service('SendCurrentState', SendCurrentState, self.addCurrentState)


    def generateBlockConfig(self, test, max = 4, min = 3):
        """ A configuration of blocks is represented as 
        a list. Each index represents a block, and the value 
        at this index represents what this block is on:
        -1 - table, 0-n: the index of the block it is on.
        MAX and MIN CANNOT be the same"""

        # check values of max and min
        if not (type(min) == types.IntType and type(max) == types.IntType):
            print "Max or Min is not an int. Using default of 3 blocks"
            min = 3
            max = 4

        if min < 0:
            print 'min must be larger than zero. Setting to 0.'
            min = 0

        if max < 0:
            print 'max must be larger than zero. Setting to 1.'
            max = 1

        if max <= min:
            print 'max must be BIGGER than min. Increasing max.'
            max = min + 1

        size = random.randrange(min, max)
        config = [-1]* size

        index = -1
        for block in config:
            index = index+1
            block_is_on_this_block = True
            block_used = True
            block_is_this_block = True


            while( block_is_on_this_block or block_is_this_block or block_used ):
                # find new value
                is_on = random.randrange(-1, size)
                block_is_this_block = (is_on == index)
                if is_on != -1:
                    block_used = (is_on in config)
                    block_is_on_this_block = (config[is_on] == index)
                else:
                    block_used = False
                    block_is_on_this_block = False

            config[index] = is_on
        # detect any loops
        array = [0]*(size+1)
        index = 0
        other = 0
        for index in range(0,size):
            other = index
            array = [0]*(size+1)
            while( True ):
                if ( config[other] == -1):
                    break;

                if ( array[other] ): # we have already been here
                    config[other] = -1
                    break;

                array[other] = 1 #we have visited this block
                other = config[other]



        # not physically possible to not have any blocks on the table
        if -1 not in config:
            config[random.randrange(-1, size)] = -1

        config = tuple(config)

        if test == 'goal':
            # print "generating a goal config"
            self.goalConfig = Configuration(config)
        else:
            # print "generating an initial config"
            self.currentState = State(Configuration(config), self.blocks )



    def sendGoalToAspModule(self):
        """ This sends goal to asp_module and returns back action.
        If we want next action we just send same goal. """

        key = (self.currentState.configuration.config, self.goalConfig.config)
        # key = ((1, 2, 1), (1, 0, 1))
        # print key
        if self.dict.has_key(key):
            prevValue = self.dict.get(key)
            if len(prevValue) != 4:
                prevValue=random.choice(list(prevValue))
            # print "yayyy"
            # print prevValue
            self.currentAction = Action(prevValue[0], prevValue[1], prevValue[2], 0, Configuration(prevValue[3]), False)
            # print self.currentAction
            return
        # else: print "nay"

        rospy.wait_for_service('AspAnswer')
        try:
            # print "asp"
            asp_answer = rospy.ServiceProxy('AspAnswer', AspAnswer)
            # print "goal"
            # print self.goalConfig
            ans = asp_answer(self.goalConfig).parsed
            self.currentAction = Action(ans.action, ans.actionableBlock, ans.destinationBlock, ans.timestep, ans.config, ans.goalAchieved)

            self.goalActive = True
            # return ans_response

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e


    def sendStateToAspModule(self):
        """ This sends the currentState to the asp module"""

        # Check validity of destination
        rospy.wait_for_service('AspCurrentState')
        # try:
        sendState = rospy.ServiceProxy('AspCurrentState', AspCurrentState)
        success = sendState(self.currentState)


        # except rospy.ServiceException, e:
        #     print "Service call failed: %s" % e
    
    def sendStateToLearningModule(self):
        rospy.wait_for_service('LMInitialise')
        try:
            sendState = rospy.ServiceProxy('LMInitialise', LMInitialise)
            success = sendState(self.currentState)
        except rospy.ServiceException, e:
            print "Service call failed %s" % e
    
    def sendActionToLearningModule(self, error):
        if error is False:
            rospy.wait_for_service('LMStateActionTaken')
            try:
                if self.currentAction.action == "put_down":
                    sendStateAction = rospy.ServiceProxy('LMStateActionTaken', LMStateActionTaken)
                    sucess = sendStateAction(self.currentAction)
            except rospy.ServiceException, e:
                print "Service call failed %s" % e

        else:   
            rospy.wait_for_service('LMErrorHasOccured')
            try:
                if self.currentAction.action == "put_down":
                    sendStateAction = rospy.ServiceProxy('LMErrorHasOccured', LMErrorHasOccured)
                    sucess = sendStateAction(self.currentAction) 
            except rospy.ServiceException, e:
                print "Service call failed %s" % e

    def sendNewBlockSetToLearningModule(self):
        rospy.wait_for_service('LMNewBlocks')
        try:
            print "sending new blocks"
            sendState = rospy.ServiceProxy('LMNewBlocks', LMNewBlocks)
            success = sendState(self.blocks)
        except rospy.ServiceException, e:
            print "Service call failed %s" % e
        
    def publisher(self, pub, msg):
        try:
            pub.publish(msg)
        except:
            print "Publishing failed call failed:"

        return
            
    def executeAction(self, action):
        """ This will send action to robot module and return feedback"""
        rospy.wait_for_service('SimulatorAddAction')
        try:
            sendState = rospy.ServiceProxy('SimulatorAddAction', SimulatorAddAction)
            state = sendState(self.currentAction)
            configuration = Configuration(state.state.configuration.config)
            self.currentState = State(configuration = configuration, block_properties = state.state.block_properties)
        except rospy.ServiceException, e:
            print "Service call failed %s" % e
        

    def addCurrentState(self, state):
        """ Gets configuration of blocks from robot"""
        print state
        

    def simulateError(self, expectedConfig):
        """if the expected configuration involved
        putting a block on a prism shaped block
        then report an error. Else report success"""

        expectedConfig = expectedConfig
        # print "simulation"
        for block in self.blocks:

            if block.label == self.currentAction.destinationBlock:
                # print block.shape 
                if block.shape == 'prism':
                    actionBlock = int(re.findall('\d+$', self.currentAction.actionableBlock)[0])
                    config = list(expectedConfig.config)
                    config[actionBlock] = -1
                    expectedConfig.config = tuple(config)
       

    def writeSequencesToList(self):
        fname = os.path.join(os.path.dirname(__file__), 'output.txt')
        key = ()
        value = []
        with open(fname) as infile:
            while("generatedRules: " not in infile.readline() ):
            
                # print "t"
                # print "whhaaaaaaaaat"

                initial = map(int, re.findall("[+-]?\d+(?:\.\d+)?", infile.readline())) 
                initial = tuple(initial)
                goal = map(int, re.findall("[+-]?\d+(?:\.\d+)?", infile.readline())) 
                goal = tuple(goal) 
                

                key = (initial, goal)
                # print "key"
                # print key

                val1 = re.findall("[a-zA-Z]*_[a-zA-Z]*", infile.readline())[0]
                val2 = re.findall("[a-zA-Z]*\d", infile.readline())[0]
                val3 = re.findall("[a-zA-Z]*\d", infile.readline())[0]
                val4 = tuple(map(int, re.findall("[+-]?\d+(?:\.\d+)?", infile.readline())))

                value = (val1, val2, val3, val4)
                # print "value"
                # print value
                # if not in dict
                if not self.dict.has_key(key):
                    # add
                    self.dict.update({key: value})
                else:
                    prevValue = self.dict.pop(key)

                    if len(prevValue) == 4:
                        prevValue = [prevValue]
                    else:
                        prevValue = list(prevValue)

                    # print prevValue
                    # check to see if value is in there
                    if value not in prevValue:
                        prevValue.append(value)
                        # print prevValue
                    self.dict.update({key: (prevValue)})




    def lookupActionSequence(self, initial, goal):



        return Action
    


########################################################################
#               Main state functions

    def initial(self):
        # print "initial"
        

        # CHECK IF NEW CONFIGURATION OF BLOCKS HAS ARRIVED
        # TO DO

        if (self.newSet is True):
            self.generateBlockConfig('hi')
            self.newSet = False
        
        print "inital config"
        print self.currentState.configuration.config
        self.goalConfig  = self.currentState.configuration



        # generate goal configuration and make sure it is different from initial
        while( self.goalConfig.config  == self.currentState.configuration.config or self.goalConfig.config == self.prevGoalConfig.config):
            self.generateBlockConfig('goal')
        print self.goalConfig.config

        self.prevGoalConfig.config = self.goalConfig.config


       
        # set up Learning Module
        if self.newSet is True:
            self.sendNewBlockSetToLearningModule()

        self.sendStateToLearningModule()

        # Now we are ready to plan
        self.state = 'plan'

    def plan(self):
        # print 'plan'

        # send inital and goal configuraton to ASP_MODULE
        self.sendStateToAspModule()
        self.sendGoalToAspModule()


        # now we are ready to execute actions
        self.state = 'execute'

    def execute(self):
        # print 'execute'

        # self.executeAction()
        print self.currentAction.action
        print self.currentAction.actionableBlock
        print self.currentAction.destinationBlock
        print self.currentAction.config.config

        self.executeAction()

        self.state = 'feedback'

    def feedback(self):
        # print 'feedback'
        
        expectedConfig = deepcopy(self.currentAction.config)
        config = deepcopy(expectedConfig)
        # print expectedConfig.config
        # config = self.getConfigBlocks() -- what we would do with real robot
        self.simulateError(config)

        # print expectedConfig.config
        # print config.config
        
        # print config.config != expectedConfig.config
  
        if config.config != expectedConfig.config:
            # print 'FAILURE'
            self.sendActionToLearningModule(True)
            self.currentState.configuration = expectedConfig
            # self.currentState.configuration = config  -- when we actually get proper feedbacko
            self.state = 'initial'
        elif config == self.goalConfig:
            # print 'GOAL'
            self.sendActionToLearningModule(False)
            self.currentState.configuration = config
            self.state = 'initial'
        else:
            print "inital config"
            print config.config
            print self.goalConfig.config
            # print 'on the way to our goooooal'
            self.sendActionToLearningModule(False)
            self.currentState.configuration = config
            self.state = 'plan'

    def learning(self):
        # print 'learning'



        self.state = 'initial'
########################################################################


if __name__ == '__main__':
    r = Robot()

    states = { 'initial': r.initial,
                'plan': r.plan,
                'execute': r.execute,
                'feedback': r.feedback,
                'learning': r.learning
            }

    car = 0
    r.executeAction()
    r.writeSequencesToList()

    while(car < 1000):
        # pass
        states[r.state]()
        car +=1

    rospy.wait_for_service('LMGenerateRules')
    try:
            getRules = rospy.ServiceProxy('LMGenerateRules', LMGenerateRules)
            rules = getRules() 
            print rules
    except rospy.ServiceException, e:
        print "Service call failed %s" % e
    
  
        

    
    timestep_publisher = rospy.Publisher('/controller/timestep', Int16, queue_size=10)
    
    observation_publisher = rospy.Publisher('/controller/observations', Observation, queue_size=10)  
    # configuration_publisher = rospy.Publisher('/controller/configuration', Configuration, queue_size=10)    
     # rate = rospy.Rate(10)
    print 'Publishers running...'
    