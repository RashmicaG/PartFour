# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:06:48 2015

@author: Prashanth
"""

"""
Inputs and Outputs:
Information is given in the form:
attr1, attr2, attr3, attr4, attr5, attr6, value
Some lines will have attr4-6 missing because they do not have any values 
corresponding to them.
Need to parse this information into corresponding attributes and value.

The output should be all rules that should be generated. As a text file (or more 
specifically an .asp file).

Pseudo-code for creating a decision tree(using C4.5 algorithm):
learning(attributes, examples):
    if len(examples) == 1:
        return this as the regression node
    elif len(attributes) == 1:
        return this as the regression node
    elif current bound < overall bound:
        overall bound = current bound
        return this as the regression node
    else:
        find best attribute using information gain:
            -- Information gain == 1/H(S)
                    where H(S) = SUM(-p*logn(p)) for n number of possiblilities.
                    p is the probability of picking an action. 
                    p = no. of times an action is chosen in a subset/ size of subset
        split up the examples into subsets (no. of values for attributes)
        remove attribute from the set of attributes
        for each value:
            child node =  call learning(attributes, subset)
            add child node to the current node

The end tree structure would be a node which has a list of children nodes.
However what we would want is a list of all child nodes which contain its parent node.
So we can traverse the tree bottom up. 
OR
We can traverse the whole tree once it is done and find all node paths that are relevant.

"""

