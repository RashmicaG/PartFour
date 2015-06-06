#!/bin/bash

INPUTFILE=$1
OUTPUTFILE=$2

#SPARC TO ASP
java -jar ~/Documents/PartFour/sparc.jar ~/Documents/PartFour/$INPUTFILE  -solver dlv 

#-solveropts "-cautious"
# #ADDING MAGIC COMMANDS
# (echo -n '#hide. # -solveropts "-pfilter=appl"
	
# 	'; cat ~/Documents/UniSummerWork/outputFiles/asp.txt) > ~/Documents/UniSummerWork/outputFiles/editedAsp.txt

# #SOLVING ASP
# dlv 0 ~/Documents/UniSummerWork/outputFiles/editedAsp.txt --shift  > ~/Documents/UniSummerWork/outputFiles/$OUTPUTFILE 
