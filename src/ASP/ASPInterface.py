#! /usr/bin/env python
import subprocess
import rospy
import os
import re
import tf
from asp_model.srv import *
from asp_model.msg import *
from tasks_common import yamlReader
from tasks_common import Translator


# TODO: move files to common

class RuleCache:

    def __init__(self):
        self.constants = []
        self.goals = []
        self.observations = []

class Door:
    def __init__(self):
        self.name = ''
        self.area = ['', '']

    def __str__(self):
        return str(self.name) + ' connected to ' + str(self.area[0]) + ', ' + str(self.area[1])


class KBInterface:
    """Used to interact withe the ASP Knowledge Base"""

    def __init__(self, solver_path, asp_path):

        # Stores rules generated in this time-step. Useful so we can look for rule duplicates/conflicts
        # self.ruleCache = RuleCache()
        self.consts = {}
        self.solver_path = solver_path
        self.asp_path = asp_path
        self.current_timestep = 0


        # self.intial_fpath = 'intialLocation.txt' # This should really be domain specific
        # self.defaults_fpath = self.domain + 'personDefaultLocation.yaml'
        # self.fpath_constants_yaml = self.domain + 'constants.yaml'
 

        #TODO: add lauch file with parameter solver path and dlv path

        # self.yr = yamlReader.YamlReader()

        rospy.init_node('AspQueryServer')
        srv_query = rospy.Service('AspQuery', AspQuery, self.queryHandler)
        srv_addrule = rospy.Service('AspAddRule', AspAddRule, self.addRuleHandler)
        srv_answer = rospy.Service('AspAnswer', AspAnswer, self.answerHandler)

        # Generate ASP rules for building
        # self.generateFiles()


        print "Ready to service queries"
        rospy.spin()

    def get_current_area(self):
        listener = tf.TransformListener()
        listener.waitForTransform("/map", "/base_link", rospy.Time(), rospy.Duration(4.0))
        trans, rot = listener.lookupTransform('/map', '/base_link', rospy.Time(0))

        area_name = self.translator.cood_to_logical(Translator.SimplePose(x=trans[0], y=trans[1], yaw=0.0))

        return self.nameToAreaMapping(area_name)




    def solve(self, status, timeStep, pfilter=''):
        """
        Solves the current knowledge base and produces answer set
        :param solverPath: location/name of the asp solver being used
        :param aspPath: location/name of merged asp file
        :return: location/name of the outputted answer set
        """


        # merge files to create KB
        self.merge(status, timeStep)

        if pfilter:
            pfilter = '-solveropts "-pfilter=' + pfilter + '"'

        fpath_answer = os.path.join(os.path.dirname(__file__), 'asp.answer')  # Where the answer set is written out
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = proc.communicate('java -jar ' + self.solver_path + '/sparc.jar ' + self.asp_path + '/merged.sp -solver dlv -A ' + pfilter + ' > ' + fpath_answer)

        return fpath_answer


    def merge(self, status, timeStep):
        """
        Grabs all the different bits of asp and merges to a single file
        :return:
        """

        fpath_constants = os.path.join(os.path.dirname(__file__), 'constants.sp')
        fpath_rules = os.path.join(os.path.dirname(__file__),'rules.sp')
        fpath_initial = os.path.join(os.path.dirname(__file__),'initial.sp')
        fpath_history = os.path.join(os.path.dirname(__file__),'history.sp')
        fpath_temp = os.path.join(os.path.dirname(__file__), 'tmp.txt')
        fpath_output = os.path.join(os.path.dirname(__file__),'merged.sp')

        if status == 'planning':
            fpath_mode= os.path.join(os.path.dirname(__file__), 'planning.sp')
            fpath_goals = os.path.join(os.path.dirname(__file__),'goal.sp')
            with open( fpath_temp, 'w') as outfile:
                with open(fpath_mode) as infile:
                    outfile.write(infile.read())
                with open(fpath_goals) as infile:
                    outfile.write(infile.read())
        else:
            fpath_mode= os.path.join(os.path.dirname(__file__), 'explanation.sp')
            with open( fpath_temp, 'w') as outfile:
                with open(fpath_mode) as infile:
                    outfile.write(infile.read())


        # # add in timestep
        # fpath_constants = os.path.join(os.path.dirname(__file__),'timestep.sp')
        # with open( fpath_constants, 'w') as outfile:
        #     for key in self.consts:
        #         outfile.write("#const " + key + " = " + str(self.consts[key]) + ". \n")
        #     outfile.write("#const numSteps = " + str(timeStep) + ".\n")



        filenames = [fpath_constants, fpath_rules, fpath_temp, fpath_initial, fpath_history]
        with open( fpath_output, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())
                if fname is fpath_constants:
                    outfile.write("#const numSteps = " + str(timeStep) + ".\n")

        print 'wooo'



    def addRuleHandler(self, rule):
        """
        Adds rules to the appropiate rule cache so that we can write them out when needed.
        Rules are kept in cache until being written out so that we can verify if new rules being added are ok.
        :param rule: The new rule that we are adding
        :return: boolean indicating success/failure
        """
        # TODO: Check for conflicting rules such as has_location(X, L), -has_location(X, L)

        if "goal(" in rule:
            #append to goal cache
            if rule not in self.ruleCache.goals:
                self.ruleCache.goals.append(rule)
                print self.ruleCache.goals
                print "goals"
                return True
            else:
                return False

        # DO NOT MOVE THIS ONE ABOVE GOALS UNLESS YOU ARE GOING TO MAKE IT SMARTER
        elif "holds(" in rule:  #assuming all observations we need to add are temporal
            #append to observation cache
            if rule not in self.ruleCache.observations:
                self.ruleCache.observations.append(rule)
                print self.ruleCache.observations
                print "observation"
                return True
            else:
                return False



    def writeRuleCache(self):


        # rewrite goals file
        fpath_goals = os.path.join(os.path.dirname(__file__),'current_goal.sp')
        with open( fpath_goals, 'w') as outfile:
            for goal in self.ruleCache.goals:
                outfile.write(goal+ "\n")

        # append observations files
        fpath_observations = os.path.join(os.path.dirname(__file__),'autogen/observations.sp')
        with open( fpath_observations, 'a') as outfile:
            for observation in self.ruleCache.observations:
                outfile.write(observation+ "\n")



    def queryHandler(self, req):
        query = req.query
        # fpath_answer = self.solve()

        f = open(fpath_answer, 'r')
        answerset = f.read()
        trueQuery = ' ' + query
        falseQuery = '-' + query

        istrue = trueQuery in answerset

        if not istrue:
            isfalse = falseQuery in answerset

        if istrue:
            return 'yes'
        elif isfalse:
            return 'no'
        else:
            return 'unknown'

    def answerHandler(self, goal):
        print goal
        fpath_goal = os.path.join(os.path.dirname(__file__), 'current_goal.sp')
        # time_step = goal.timeStep
        time_step = 0
        goal = self.generate_goal(goal)

        with open(fpath_goal, 'w') as outfile:
            outfile.writelines(goal)

        tries=0
        while(tries <10):
             #  Solve and read
            fpath_answer = self.solve('planning', time_step, pfilter='occurs')
            self.current_timestep = int(time_step)-1
            with open(fpath_answer, 'r') as infile:
                answer_string = infile.read()
                # if blank file (ie inconsistent)
                print answer_string
                if os.stat(fpath_answer).st_size >2:
                    return self.parse_answer(answer_string)
                else:
                    tries += 1
                    time_step += 1
                    print tries
        # add is stuff for explanations





    def generate_goal(self, goal):
        # asp.goal = 'goal(I) :- holds(is_on(block3, s1), I), holds(is_on(block2, s3), I).'
        asp_goal = 'goal(I) :- holds(on(block2, s5), I),holds(on(block3, s4), I), holds(on(block4, s0), I).'

        return asp_goal


    def parse_answer(self, raw):
        parsed = []  # Use this to save list of SubGoals
        raw = re.findall("\{(.*?)\}", raw)  # The answer set is inside the squiggly brackets {}
        raw = raw[0]
        raw = raw.replace(' ', '')
        anslist = raw.split('occurs')

        for step in anslist:
            if step:
                operation = re.findall("\((.*?)\(", step)  # op
                time_step = re.findall("\)(.*)\)", step)  # get the timestep
                time_step = time_step[0].replace(',', '')    # remove the comma from timestep
                temp = re.search("\((.*)\)", step).group(1)  # remove the outer brackets from statement
                target = re.findall("\((.*)\),", temp)  # grab stuff within the remain beackets (target)
                parsed.append(SubGoal(operation=operation[0], target=self.aspToRealMapping(target[0]), time_step=int(time_step)))

        return AspAnswerResponse(parsed=parsed)

if __name__ == "__main__":

    sparc_path = sys.argv[1]
    asp_path = sys.argv[2]
    kb = KBInterface(sparc_path, asp_path)
    
     # kb.solve(pfilter='occurs')

    # kb.addRuleHandler("numDoors")
    # kb.addRuleHandler("holds(door_open(d1,true)).")
    # kb.addRuleHandler("goal :- holds(blah, I).")
    # kb.addRuleHandler("numRooms")
    # kb.addRuleHandler("holds(door_open(d3,true)).")
    # kb.addRuleHandler("goal :- holds(blahblah, I).")
    #
    # kb.writeRuleCache()
    #
    # kb.merge('explanation')
    kb.answerHandler('asdf')

    # kb.solve(5, "pfilter= occurs")

    # kb.doorsToObservations()


