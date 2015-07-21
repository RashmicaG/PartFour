#! /usr/bin/env python
import subprocess
import rospy
import os
import re
import tf
from asp_module.srv import *
from asp_module.msg import *
from threading import Thread
from std_msgs.msg import Int16


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


class ASPInterface:
    """Used to interact withe the ASP Knowledge Base"""

    def __init__(self, solver_path, asp_path):

        # Stores rules generated in this timestep. Useful so we can look for rule duplicates/conflicts
        # self.ruleCache = RuleCache()
        self.solver_path = solver_path
        self.asp_path = asp_path
        self.current_timestep = 0
        self.current_plan = []
        self.goal = 'null'
        self.iterator = 0
        self.timestep = 0
        self.observations = []

        #TODO: add lauch file with parameter solver path and dlv path

        rospy.init_node('AspServer')
        # srv_query = rospy.Service('AspQuery', AspQuery, self.queryHandler)
        srv_addObs = rospy.Service('AspAddObservation', AspAddObservation, self.addObservationHandler)
        srv_answer = rospy.Service('AspAnswer', AspAnswer, self.answerHandler)


    def solve(self, mode, timeStep, pfilter='', goal=''):
        """
        Solves the current knowledge base and produces answer set
        :param solverPath: location/name of the asp solver being used
        :param aspPath: location/name of merged asp file
        :return: location/name of the outputted answer set
        """
        # merge files to create kb
        self.merge(mode, timeStep)

        if pfilter:
            pfilter = '-solveropts "-pfilter=' + pfilter + '"'

        fpath_answer = os.path.join(os.path.dirname(__file__), 'asp.answer')  # Where the answer set is written out
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = proc.communicate('java -jar ' + self.solver_path + '/sparc.jar ' + self.asp_path + '/merged.sp -solver dlv -A ' + pfilter + ' > ' + fpath_answer)

        return fpath_answer


    def merge(self, mode, timeStep):
        """
        Grabs all the different bits of asp and merges to a single file
        :return:
        """
        try:

            fpath_constants = os.path.join(os.path.dirname(__file__), 'constants.sp')
            fpath_rules = os.path.join(os.path.dirname(__file__),'rules.sp')
            fpath_initial = os.path.join(os.path.dirname(__file__),'initial.sp')
            fpath_history = os.path.join(os.path.dirname(__file__),'history.sp')
            fpath_output = os.path.join(os.path.dirname(__file__),'merged.sp')
            fpath_planner= os.path.join(os.path.dirname(__file__), 'planning.sp')
            fpath_explainer= os.path.join(os.path.dirname(__file__), 'explanation.sp')
            fpath_goal = os.path.join(os.path.dirname(__file__),'goal.sp')

            filenames = [fpath_constants, fpath_rules, fpath_initial, fpath_history]
           
            if mode == 'planning':
                filenames.append(fpath_planner)
                # if goal != '':
                #     filenames.append(fpath_goal)
            elif mode == 'explaining':
                filenames.append(fpath_explainer)


            with open( fpath_output, 'w') as outfile:
                for fname in filenames:
                    with open(fname) as infile:
                        outfile.write(infile.read())
                    if fname is fpath_constants:
                        outfile.write("#const numSteps = " + str(timeStep) + ".\n")
                    elif fname is fpath_planner:
                        outfile.write(self.goal)
        except:
            print "Merging ASP files failed"

    def addObservationHandler(self, observation):
        pass


    def querySurface(self, surface):
        """ This function takes a surface and returns 
        the object that this surface belongs to"""
        try:
            pattern = 'has_surface(.*?, ' + surface + ').'
            fpath_initial = os.path.join(os.path.dirname(__file__), 'initial.sp')
            for line in open(fpath_initial):
                for match in re.findall(pattern, line):
                    # isolate block
                    block = re.findall("\((.*),", match)[0]
                    return block
        except:
            print "Error in querySurface()"


    def answerHandler(self, goal=''):
        """ Function called when a node calls AspAnswer service.
        Attempts to generate a plan for the goal that is given."""
        if goal.goal != self.goal:
            try:
                print 'new goal!'
                self.goal = goal.goal
                self.iterator = 0
                timestep = self.timestep
                max_timestep = 10

                while(timestep <max_timestep):
                     #  Solve and read
                    fpath_answer = self.solve('planning', timestep, pfilter='occurs')
                    with open(fpath_answer, 'r') as infile:
                        raw = infile.read()
                        self.parse_answer(raw)
                        print self.current_plan
                    if not self.current_plan:
                        timestep += 1
                    else:
                       return AspAnswerResponse(parsed=self.current_plan[self.iterator])
             except:
                print "An error occured in answerHandler"
        else:
            try:
                print 'same goal!'
                self.iterator += 1
                return AspAnswerResponse(parsed=self.current_plan[self.iterator])
            except IndexError:
                return AspAnswerResponse(parsed= Action(action = 'null', actionableBlock = 'null', destinationBlock = 'null', timestep=0, goalAchieved = True))
            


    def parse_answer(self, raw):
        """ This parses an answer set, looking for actions with blocks"""
        parsed =[] # Use this to save list of SubGoals
        if len(raw) <2:
            pass
        else:
            raw = re.findall("\{(.*?)\}", raw)[0]  # The answer set is inside the squiggly brackets {}
            # remove spaces between steps
            raw = raw.replace(' ', '')
            # remove occurs and save steps in a list
            anslist = raw.split('occurs')

            for step in anslist:
                if step:
                    # get action
                    action = re.findall("\((.*?)\(", step)[0]  
                    # get the timestep
                    timestep = re.findall("\)(.*)\)", step) 
                    # remove the comma from timestep 
                    timestep = timestep[0].replace(',', '')   
                    # remove the outer brackets from statement
                    temp = re.search("\((.*)\)", step).group(1)  
                    # remove brackets
                    target = re.findall("\((.*)\),", temp)[0]
                    # put arguments into a list
                    arglist = target.split(',')
                    # we can ignore first element for now, as we are only dealing with one agent
                    block = arglist[1]
                    if action == 'put_down':
                        surface = arglist[2]
                        # find out which object the surface belongs to
                        destBlock = self.querySurface(surface)
                    else:
                        destBlock = 'null'

                    parsed.insert(int(timestep),(Action(action = action, actionableBlock = block, destinationBlock = destBlock, timestep=int(timestep), goalAchieved = False)))

        self.current_plan = parsed
        return 



    def newTimestepCallback(self, timestep):
        """New timestep"""
        print 'A new timestep has just come in!'
        self.timestep = timestep.data
        print 'timestep is now ' 
        print self.timestep
        return

    def newObservationCallback(self, observation):
        """ Add new observation to observation queue """
        self.observations.append(observation)
        self.checkNewObservations()
        

    def newGoalCallback(self, goal):
        pass # don't think we will need this

    def checkNewObservations(self):
        """ Checks if new observations are valid
        observation type and then appends them."""
        if len(self.observations) > 0:
            unparsedObs = self.observations.pop()
            parsedObs='holds('

            if not unparsedObs.negation:
                parsedObs= '-' + parsedObs

            parsedObs += unparsedObs.fluent + '(' + unparsedObs.argument1 + ',' + unparsedObs.argument2 + '),' + str(unparsedObs.timestep) + ').'
            print parsedObs

        else:
            return


if __name__ == "__main__":

    sparc_path = sys.argv[1]
    asp_path = sys.argv[2]
    kb = ASPInterface(sparc_path, asp_path)

    rospy.Subscriber('/controller/timestep', Int16, kb.newTimestepCallback)
    # rospy.Subscriber('/controller/goal', Goal, kb.newGoalCallback)
    rospy.Subscriber('/controller/observations', Observation, kb.newObservationCallback)

    print "Ready to service queries"

    kb.checkNewObservations()
    rospy.spin()
    
   
    # kb.merge('explanation')
    # kb.answerHandler('asdf')
    # print kb.current_plan

    # kb.solve(5, "pfilter= occurs")

    # kb.doorsToObservations()


