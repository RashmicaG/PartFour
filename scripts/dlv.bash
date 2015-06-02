#!/bin/bash

INPUTFILE=$1
OUTPUTFILE=$2

#SPARC TO ASP
java -jar ~/Documents/PartFour/sparc.jar ~/Documents/PartFour/sparcFiles/$INPUTFILE  -solver dlv  #-A  -solveropts "-pfilter=occurs" -o ~/Documents/UniSummerWork/outputFiles/asp.txt > ~/Documents/UniSummerWork/outputFiles/output.txt


#-solveropts "-cautious"
# #ADDING MAGIC COMMANDS
# (echo -n '#hide. # -solveropts "-pfilter=appl"
	
# 	'; cat ~/Documents/UniSummerWork/outputFiles/asp.txt) > ~/Documents/UniSummerWork/outputFiles/editedAsp.txt

# #SOLVING ASP
# dlv 0 ~/Documents/UniSummerWork/outputFiles/editedAsp.txt --shift  > ~/Documents/UniSummerWork/outputFiles/$OUTPUTFILE 
