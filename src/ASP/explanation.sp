
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Explanation Module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% %% %% Take what actually happened into account:
occurs(A,I) :- hpd(A,I).

%% Reality Check 
:- obs(F,true,I), -holds(F,I).
:- obs(F,false,I), holds(F,I).

expl(A,I) :- #exogenous_action(A),
             occurs(A,I),
             not hpd(A,I).

%%   MINIMAL EXPLANATIONS:                            
occurs(A,K) :+ #exogenous_action(A),
              K >= (numSteps-3), K < numSteps.
