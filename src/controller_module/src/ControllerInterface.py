#!/usr/bin/env python

import rospy
from asp_module.srv import *
from asp_module.msg import *
from std_msgs.msg import Int16

class Robot:
    def __init__(self):
        self.timestep = 1
        self.goalActive = False
        self.nextAction = 'null'

    def get_answer_set(self, data):
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



if __name__ == '__main__':
    rospy.init_node('controller', anonymous=True)
    r = Robot()

    
    timestep_publisher = rospy.Publisher('/controller/timestep', Int16, queue_size=10)
    observation_publisher = rospy.Publisher('/controller/observations', Observation, queue_size=10)   
     # rate = rospy.Rate(10)
    print 'Publishers running...'

    # holds(on(block1, s2), 0).
   
    r.get_answer_set('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    r.get_answer_set('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    r.publisher( timestep_publisher, r.timestep)
    r.get_answer_set('goal(I) :- holds(on(block0, s5), I), holds(on(block1, s2), I), holds(on(block2, s5), I), holds(on(block3, s4), I), holds(on(block4, s0), I).')
    
    obs = (Observation(negation=False, fluent='on', argument1='block1', argument2='s2', timestep=r.timestep))
    print obs
    r.publisher(observation_publisher, obs)

    # while not rospy.is_shutdown():
        # rate.sleep()
