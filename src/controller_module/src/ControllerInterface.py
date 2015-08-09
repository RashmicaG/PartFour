#!/usr/bin/env python

import rospy
from asp_module.srv import *
from asp_module.msg import *
from asp_module import *
from std_msgs.msg import Int16
from collections import deque
from controller_module.msg import *
import random
import types


class Robot:
    def __init__(self):
        self.state = 'initial'
        self.timestep = 1
        self.goalActive = False
        self.goalQueue = [] # how to initialise queue.?
        self.goalConfig = Configuration([])
        self.currentState = State(Configuration([]), [] )
        self.currentAction = Action('null', 'null', 'null', 0, Configuration([]),  False)

        self.block = Block('h1', 'sdf', 'asdfas', 'asdf')



    def sendGoal(self):
        """" This is the start of each iteration. Should we update timestep here?
        hmmmmm"""
        try:
            # If nothing in goalQueue then generate random goal
            if not self.goalQueue:
                self.sendGoalToAspModule(self.generateGoal())
            else:
                self.sendGoalToAspModule(self.goalQueue.popleft())
        except:
            print "sendGoal failed"



    def generateBlockConfig(self, test, max = 5, min = 4 ):
        """ A configuration of blocks is represented as 
        a list. Each index represents a block, and the value 
        at this index represents what this block is on:
        -1 - table, 0-n: the index of the block it is on.
        MAX and MIN CANNOT be the same"""

        # check values of max and min
        if not (type(min) == types.IntType and type(max) == types.IntType):
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
            block_is_on_this_block = True
            block_used = True
            block_is_this_block = True


            while( block_is_on_this_block or block_is_this_block or block_used ):
                # find new value
                print 'index ' + str(index)
                is_on = random.randrange(-1, size)
                block_is_this_block = (is_on == index)
                print is_on
                if is_on != -1:
                    block_used = (is_on in config)
                    block_is_on_this_block = (config[is_on] == index)
                else:
                    block_used = False
                    block_is_on_this_block = False
                
                print block_is_this_block
                print block_is_on_this_block
                print block_used

            config[index] = is_on
        print config
        print "loop detection"
        # detect any loops
        array = [0]*(size+1)
        index = 0
        other = 0
        for index in range(0,size):
            other = index
            array = [0]*(size+1)
            while( True ):
                print array
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

        print config
 
        # only for testing purposes
        blocks = [Block('block0', 'cuboid', 'small', 'blue'), 
                    Block('block1', 'prism', 'small', 'red'), 
                    Block('block2', 'cube', 'small', 'blue'), 
                    Block('block3', 'cube', 'small', 'red'),
                    # Block('block4', 'prism', 'small', 'yellow')
                    ]

        # print blocks

        if test == 'goal':
            print "generating a goal config"
            self.goalConfig = Configuration(config)
        else:
            print "generating an initial config"
            self.currentState = State(Configuration(config), blocks )

       



    def sendGoalToAspModule(self):
        """ This sends goal to asp_module and returns back action.
        If we want next action we just send same goal. """
        rospy.wait_for_service('AspAnswer')
        try:
            asp_answer = rospy.ServiceProxy('AspAnswer', AspAnswer)
            print self.goalConfig
            self.currentAction = asp_answer(self.goalConfig)

            print self.currentAction

            self.goalActive = True
            # return ans_response

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e


    def sendStateToAspModule(self):
        """ This sends the currentState to the asp module"""

        # Check validity of destination
        rospy.wait_for_service('AspCurrentState')
        try:
            sendState = rospy.ServiceProxy('AspCurrentState', AspCurrentState)
            success = sendState(self.currentState)


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


########################################################################
#               Main state functions

    def initial(self):
        print "initial"
        

        # CHECK IF NEW CONFIGURATION OF BLOCKS HAS ARRIVED
        # TO DO
        self.generateBlockConfig('hi')
        self.goalConfig  = self.currentState.configuration

        # generate goal configuration and make sure it is different from initial
        while( self.goalConfig  == self.currentState.configuration):
            self.generateBlockConfig('goal')

        # Now we are ready to plan
        self.state = 'plan'

    def plan(self):
        print 'plan'

        # send inital and goal configuraton to ASP_MODULE
        self.sendStateToAspModule()
        self.sendGoalToAspModule()

        # send inital and goal configuraton to LEARNING_MODULE -- ON POLICY

        # now we are ready to execute actions
        self.state = 'execute'

    def execute(self):
        print 'execute'

        # when no answer set, this breaks. FIX
        while(not self.currentAction.parsed.goalAchieved):
            print self.sendGoalToAspModule()


        self.state = 'feedback'

    def feedback(self):
        print 'feedback'

        if config != expectedConfig:
            print 'FAILURE'
        elif config == goalConfig:
            print 'GOAL"'
        else:
            print 'on the way to our goooooal'
        self.state = 'learning'

    def learning(self):
        print 'learning'

        # send inital and goal configuraton to LEARNING_MODULE -- OFFPOLICY


        self.state = 'initial'
########################################################################


if __name__ == '__main__':
    rospy.init_node('controller', anonymous=True)
    r = Robot()

    states = { 'initial': r.initial,
                'plan': r.plan,
                'execute': r.execute,
                'feedback': r.feedback,
                'learning': r.learning
            }

    car = 0

    while(car<4):
        # pass
        states[r.state]()
        car +=1

    
    timestep_publisher = rospy.Publisher('/controller/timestep', Int16, queue_size=10)
    
    observation_publisher = rospy.Publisher('/controller/observations', Observation, queue_size=10)  
    # configuration_publisher = rospy.Publisher('/controller/configuration', Configuration, queue_size=10)    
     # rate = rospy.Rate(10)
    print 'Publishers running...'
    


    # r.sendGoalToAspModule('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    # r.sendGoalToAspModule('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    # r.publisher( timestep_publisher, r.timestep)
    # r.sendGoalToAspModule('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    # 
    # holds(on(block1, s2), 0).
    # obs = (Observation(negation=False, fluent='on', argument1='block1', argument2='s2', timestep=r.timestep))

    # print 'obs sent :'
    # print obs
    # r.publisher(observation_publisher, obs)

    # while not rospy.is_shutdown():
        # rate.sleep()
