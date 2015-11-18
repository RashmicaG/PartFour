
You need the following installed:
- ROS -- indigo or later (should work fine on earlier versions but hasn't been tested)
- SPARC (https://github.com/iensen/sparc/wiki)
- DLV (http://www.dlvsystem.com/). This needs to be executable from the folder you run the code from.
- python with pygame, numpy and scipy.


Running the code:
Run each of the following in a separate terminal:
- rosrun asp\_module ASPInterface.py path_to_SPARC_solver  path_to_catkin_workspace/src/asp_module/src/
- rosrun controller_module ControllerInterface.py 
- rosrun learning_module LearningModule.py 
- rosrun simulator_module Simulator.py 

If you want to use a robot arm instead you can create a Robot module to replace the simulator module.
