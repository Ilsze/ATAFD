#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATAFD: version 1
2/12/21

Model Parameters: timefactor, stagnationfactor, numagents, numtasks, foxhedgeratio, penalty, scorecoeff

Classes: Agents, tasks, blackboard


Functions: Main, Initilzation, MoveTask, MoveAgent, Assign, AssignUnclaimed, AssignNew, AgentsWork, MakeCompetiters, Reassign
"""

import numpy as np
import matplotlib.pyplot as plt
import random

#just an example
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("John", 36)
p2 = Person()

print(p1.name)
print(p1.age)

#classes:
"""
Agents: 
    attributes:skillStrength
    
""" 

class Agent:
    skillStength = 0.0
    
"""
"""

class Task:
    type = 0
"""
"""
class Blackboard:
    numTasks = 50
    
        
#methods (functions):
    
"""
"""    
def Initialization():
   
"""
Paramters (Type Name): 
    Task toBeMoved - task to me moved
    List[Task] source - list it's being moved from
    List[Task] destination - list it's being moved to
"""   
def MoveTask(toBeMoved, source, destination)): 
    
"""
Parameters (Type Name):
    Agent toBeMoved
    List[Agent] source
    List[Agent] destination
"""   
def MoveAgent(toBeMoved, source, destination): 
    
"""
Parameters (Type Name):
    List[Agent] agentSource
    List[Agent] busyAgents
    List[Task] taskSource
    List[Task] claimedTasks
"""   
def Assign(agentSource, busyAgents, taskSource, claimedTasks):

"""
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] busyAgents
    List[Task] unclaimedTasks
    List[Task] claimedTasks
"""     
def AssignUnclaimed(idleAgents, busyAgents, unclaimedTasks, claimedTasks):
    
"""
May add an AssignNew function later
"""    
#def AssignNew():
    
"""
"""     
def AgentsWork():
    
"""
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] competingAgents
"""    
def MakeCompetitors(idleAgents, competingAgents):
    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] idleAgents
"""    
def RemoveCompetitors(competingAgents, idleAgents):
    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] claimedTasks
    List[Agents] busyAgents
"""    
def Reassign(competingAgents, claimedTasks, busyAgents):
    
"""
"""     
def main(timefactor, stagnationfactor, numagents, numtasks, foxhedgeratio, penalty, scorecoeff):
    
    timer = 0
    stagnationTimer = stagnationfactor

    #Initialization()

    #start simulation loop



    
    
    
main()

