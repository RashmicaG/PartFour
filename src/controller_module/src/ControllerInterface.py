
import rospy
from asp_module.srv import *

class Robot:
    def get_answer_set(self, data, time_step):
        rospy.wait_for_service('AspAnswer')
        try:
            asp_answer = rospy.ServiceProxy('AspAnswer', AspAnswer)
            print time_step
            ans_response = asp_answer()

            print ans_response

            self.goalActive = True
            return ans_response.parsed

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e



if __name__ == '__main__':
    r = Robot()

    r.get_answer_set('asdfa', 0)
