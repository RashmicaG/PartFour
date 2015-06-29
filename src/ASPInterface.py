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
        # self.consts = {}
         self.solver_path = solver_path
         self.asp_path = asp_path
         self.current_timestep = 0

        # self.domain = 'domains/newmarket3/'
        # self.locations_file = self.domain + 'locations.yaml'
        # self.map_file = self.domain + 'newmarket3.yaml'
        # self.door_file = self.domain + 'doors.yaml'

        # self.intial_fpath = 'intialLocation.txt' # This should really be domain specific
        # self.areasList_fpath = self.domain + 'areasList.yaml'
        # self.doorslist_fpath = self.domain + 'doorsList.yaml'
        # self.defaults_fpath = self.domain + 'personDefaultLocation.yaml'
        # self.fpath_constants_yaml = self.domain + 'constants.yaml'
        # self.areasRooms_fpath = self.domain + 'areasInRooms.yaml'

        # self.translator = Translator.LogicalTranslator(self.map_file, self.locations_file, self.door_file)

    

        #TODO: add lauch file with parameter solver path and dlv path

        self.yr = yamlReader.YamlReader()

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

    # def generateFiles(self):

    #     # take info from doors.yaml and convert to a form usable for ASP
    #     fpath_output = os.path.join(os.path.dirname(__file__), 'autogen/observations.sp')
    #     fpath_doors_auto = os.path.join(self.yr.path, 'autogen/doorsList.sp')

    #     doorArray = []
    #     areaArray = []
    #     roomArray = []

    #     areaYaml = self.yr.YamlIntoDict(self.areasList_fpath)
    #     with open(fpath_output, 'w') as outfile:
    #         doorYaml = self.yr.YamlIntoDict(self.door_file)
    #         # for each door, save the approach locations so we can add observations to KB
    #         for d in doorYaml:
    #             temp = Door()
    #             for a in range(0 , 2):
    #                 # save door name
    #                 door = d['name']
    #                 # save approach location
    #                 area = d['approach'][a]['from']
    #                 # add info to array
    #                 temp.name = door
    #                 temp.area[a] = area
    #             doorArray.append(temp)

    #         # add robots initial location in
    #         fpath_initial_location = os.path.join(os.path.dirname(__file__), self.intial_fpath)

    #         with open(fpath_initial_location, 'r') as initial:
    #             # current_area = self.get_current_area()
    #             current_area = 'a8'
    #             # print 'Generating file with current area as: ' + str(current_area)
    #             outfile.write('holds(robot_location(' + str(current_area) + '),0).')

    #         # add observations into KB for areas in rooms
    #         areaRoomYaml = self.yr.YamlIntoDict(self.areasRooms_fpath)
    #             # find the room that the area is in
    #         for area in areaRoomYaml:
    #             if area not in areaArray:
    #                 areaArray.append(area)
    #             room = areaRoomYaml[area]
    #             outfile.write(" is_in_room(" + area + "," + room + "). \n")
    #             if room not in roomArray:
    #                 roomArray.append(room)

    #         print 'arealen = ' + str(len(areaArray))

    #         # save door keys to the door names
    #         for door in doorArray:
    #             # get keys of areas
    #             key0 = areaYaml.keys()[areaYaml.values().index(door.area[0])]
    #             key1 = areaYaml.keys()[areaYaml.values().index(door.area[1])]
    #             outfile.write( " has_door(" + areaRoomYaml[key0] + "," + "d" + str(doorArray.index((door))+1) + "). " + "\n")
    #             outfile.write(" has_door(" + areaRoomYaml[key1] + "," + "d" + str(doorArray.index((door))+1) + ")"
    #                                                                                                 ". " + "\n")

    #         # save people and their default locations
    #         fpath_temp = os.path.join(os.path.dirname(__file__), 'tmp.txt')
    #         defaultsYaml = self.yr.YamlIntoDict(self.defaults_fpath)
    #         personList = "#person = {"
    #         lastPerson = ""
    #         for i, person in enumerate(defaultsYaml):
    #             rule = "holds(has_location(" + person + "," + defaultsYaml[person] + "),I) :+ happened(person_lost(" + person + "), I). \n"
    #             rule = rule + "holds(has_location(" + person + "," + defaultsYaml[person] + "),0). \n"
    #             outfile.write(rule)
    #             personList = personList + person;
    #             if i < len(defaultsYaml)-1:
    #                 personList += ", "
    #         personList = personList + "}. \n"
    #         with open( fpath_temp, 'w') as outfile_tmp:
    #             outfile_tmp.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    #             outfile_tmp.write("sorts\n")
    #             outfile_tmp.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    #             outfile_tmp.write(personList)


    #     with open(fpath_doors_auto, 'w') as outfile_door:
    #         # add doors into doorsList.txt
    #         for door in doorArray:
    #             outfile_door.write("d" + str(doorArray.index((door))+1) + " : " + door.name + "\n")

    #     # initialise constants file
    #     fpath_changing_constants = os.path.join(os.path.dirname(__file__), 'changing_constants.sp')
    #     with open(fpath_changing_constants, 'w') as outfile:
    #         self.consts = self.yr.YamlIntoDict(self.fpath_constants_yaml)
    #         for key in self.consts:
    #             if key == "numDoors":
    #                 self.consts[key] = len(doorArray)
    #             elif key == "numRooms":
    #                 self.consts[key] = len(roomArray)
    #             elif key == "numAreas":
    #                 self.consts[key] = len(areaArray)
    #             outfile.write("#const " + key + " = " + str(self.consts[key]) + ". \n")




    def solve(self, timeStep, pfilter=''):
        """
        Solves the current knowledge base and produces answer set
        :param solverPath: location/name of the asp solver being used
        :param aspPath: location/name of merged asp file
        :return: location/name of the outputted answer set
        """

        # add timeStep to constants
        fpath_constants = os.path.join(os.path.dirname(__file__),'changing_constants.sp')
        with open( fpath_constants, 'w') as outfile:
            for key in self.consts:
                outfile.write("#const " + key + " = " + str(self.consts[key]) + ". \n")
            outfile.write("#const numSteps = " + str(timeStep) + ".\n")


        # merge files to create KB
        self.merge()

        if pfilter:
            pfilter = '-solveropts "-pfilter=' + pfilter + '"'

        fpath_answer = os.path.join(os.path.dirname(__file__), 'asp.answer')  # Where the answer set is written out
        proc = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = proc.communicate('java -jar ' + self.solver_path + ' ' + self.asp_path + ' -A ' + pfilter + ' > ' + fpath_answer)

        return fpath_answer


    # def merge(self):
    #     """
    #     Grabs all the different bits of asp and merges to a single file
    #     :return:
    #     """

    #     fpath_constants = os.path.join(os.path.dirname(__file__), 'changing_constants.sp')
    #     fpath_constants = os.path.join(os.path.dirname(__file__), 'changing_constants.sp')
    #     fpath_static_rules = os.path.join(os.path.dirname(__file__),'basic_knowledge_base.asp')
    #     fpath_goals = os.path.join(os.path.dirname(__file__),'current_goal.sp')
    #     fpath_observations = os.path.join(os.path.dirname(__file__),'autogen/observations.sp')
    #     fpath_temp = os.path.join(os.path.dirname(__file__), 'tmp.txt')
    #     fpath_output = os.path.join(os.path.dirname(__file__),'merged.sp')

    #     filenames = [fpath_constants, fpath_temp, fpath_static_rules, fpath_goals, fpath_observations]
    #     with open( fpath_output, 'w') as outfile:
    #         for fname in filenames:
    #             with open(fname) as infile:
    #                 outfile.write(infile.read())



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
        time_step = goal.timeStep
        goal = self.generate_goal(goal)

        with open(fpath_goal, 'w') as outfile:
            outfile.writelines(goal)

        tries=0
        while(tries <10):
             #  Solve and read
            fpath_answer = self.solve(time_step, pfilter='occurs')
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





    def generate_goal(self, goal):
        asp.goal = 'goal(I) :- holds(is_on(block3, s1), I), holds(is_on(block2, s3), I).'
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
    
     kb.solve(pfilter='occurs')

    # kb.addRuleHandler("numDoors")
    # kb.addRuleHandler("holds(door_open(d1,true)).")
    # kb.addRuleHandler("goal :- holds(blah, I).")
    # kb.addRuleHandler("numRooms")
    # kb.addRuleHandler("holds(door_open(d3,true)).")
    # kb.addRuleHandler("goal :- holds(blahblah, I).")
    #
    # kb.writeRuleCache()
    #
    # kb.merge()

    # kb.solve(5, "pfilter= occurs")

    # kb.doorsToObservations()


