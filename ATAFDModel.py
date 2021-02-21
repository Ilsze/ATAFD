#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATAFD: version 1
2/12/21

Model Parameters: timefactor, stagnationfactor, numagents, numtasks, foxhedgeratio, penalty, scorecoeff

Classes: Agents, Tasks, Blackboard


Functions: Main, Initilzation, MoveTask, MoveAgent, Assign, AssignUnclaimed, AssignNew, AgentsWork, MakeCompetiters, Reassign
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from random import randint
import math



#classes:
"""
Agents: 
    attributes (Type Name): Float skillStrength, Set[Integer] skillType , Integer ID    
""" 

class Agent:
    def __init__(self, ID, skillLength):
        self.ID = ID
        self.skillLength = skillLength
      
        self.skillType = set()
        
        #generate list of skill types
        length = 0
        while length < skillLength:
            self.skillType.add(randint(0, 9))
            length =  len(self.skillType)
                
    
"""
Tasks:
    attributes (Type Name): Integer taskType, Integer agentAssigned, Float timeRequired, Float pendingTimerequired
"""

class Task:
     def __init__(self):
        self.taskType = randint(0, 9)
        #set to -1 when no agent is assigned
        self.agentAssigned = -1
        #set to -1 before task has been started by an agent
        self.timeRequired = -1
        
       
        
        
        
            
"""
Blackboard:
    attributes (Type Name): Integer numTasks, List[Agent] idleAgents, List[Agent] busyAgents, List[Agent] competingAgents, List[Task] unclaimedTasks, 
    List[Task] completedTasks
"""
class Blackboard:
     def __init__(self, numtasks):
        self.numTasks = numtasks
        self.idleAgents = []
        self.busyAgents = []
        self.competingAgents = []
        self.unclaimedTasks = []
        self.claimedTasks = []
        self.completedTasks = []
    
    
        
#methods (functions):
    
"""
Initialization:
Parameters (Type Name):
    Integer numagents - number of agents in simulation
    Integer numtasks - number of tasks in simulation
    Float foxhedge - the percentage of fox agents (ie. 0.2)
"""    
def Initialization(blackboard, numAgents, numTasks, foxHedge, timeFactor):
    
    #determine number of foxes and hedges from foxhedge ratio
    numFox = int(numAgents*foxHedge)
    numHedge = int(numAgents*(1-foxHedge))
    
    #generate number of skills for each fox with uniform distribution
    skillLength = np.random.randint(low = 2, high = 9, size = numFox)
    #create foxes
    for i in range(numFox):
        #create fox agents and append them to the list of idle agents 
        blackboard.idleAgents.append(Agent(i, skillLength[i]))
        
    for i in range(numHedge):
        #create hedgehog agents and append them to the list of idle agents 
        blackboard.idleAgents.append(Agent(i+numFox, 1))
        
    #shuffle list of agents
    blackboard.idleAgents = random.shuffle(blackboard.idleAgents)
    
    #generate tasks
    for i in range(numTasks):
        blackboard.unclaimedTasks.append(Task())
    
       


"""
MoveTask:
Paramters (Type Name): 
    Task toBeMoved - task to me moved
    List[Task] source - list it's being moved from
    List[Task] destination - list it's being moved to
"""   
def MoveTask(toBeMoved, source, destination): 
    ##if toBeMoved in source:
    #remove task from source list
    source.remove(toBeMoved)
    #add task to destination list
    destination.append(toBeMoved)
    
"""
MoveAgent:
Parameters (Type Name):
    Agent toBeMoved - agent to be moved
    List[Agent] source - list agent is being removed from
    List[Agent] destination - list agent is being moved to
    
"""   

def MoveAgent(toBeMoved, source, destination): 
    #remove agent from source list
    source.remove(toBeMoved)
    #add agent to destination list
    destination.append(toBeMoved)
    
"""
Assign:
Parameters (Type Name):
    List[Agent] agentSource
    List[Agent] busyAgents
    List[Task] taskSource
    List[Task] claimedTasks
"""   
def Assign(agentSource, busyAgents, taskSource, claimedTasks, timeFactor):
    #agents iterate through task list and take the first eligible match
    if agentSource is not None:
        for agent in agentSource:
            if taskSource is not None:
                for task in taskSource:
                    #if task type matches agent type
                    if task.taskType in agent.skillType: 
                        #set task's assigned agent to agent ID
                        task.agentAssigned = agent.ID
                        task.timeRequired = timeFactor*agent.skillLength
                        MoveTask(task, taskSource, claimedTasks)
                        MoveAgent(agent, agentSource, busyAgents)
                

"""
AssignUnclaimed:
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] busyAgents
    List[Task] unclaimedTasks
    List[Task] claimedTasks
"""     
def AssignUnclaimed(idleAgents, busyAgents, unclaimedTasks, claimedTasks, timeFactor):
    Assign(idleAgents, busyAgents, unclaimedTasks, claimedTasks, timeFactor)
    
    
"""
May add an AssignNew function later
"""    
#def AssignNew():
    
"""
"""     
def AgentsWork(busyAgents, idleAgents, claimedTasks, completedTasks, stagnationTimer):
    if claimedTasks is not None:
        print("claimedTasks is not empty")
    for task in claimedTasks:
        print("time required: ", task.timeRequired)
        #work on task by subtracting 1
        task.timeRequired = task.timeRequired - 1
        
        if task.timeRequired == 0:
            if task in claimedTasks:
                print("task is in claimedTask")
            MoveTask(task, claimedTasks, completedTasks)
            for agent in busyAgents:
                if agent.ID == task.assignedAgent:
                    completer = agent
            MoveAgent(completer, busyAgents, idleAgents)
        else:
              stagnationTimer = stagnationTimer + 1
"""
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] competingAgents
"""    
def MakeCompetitors(idleAgents, competingAgents):
    if idleAgents is not None:
        for agent in idleAgents:
        	MoveAgent(agent, idleAgents, competingAgents)

    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] idleAgents
"""    
def RemoveCompetitors(competingAgents, idleAgents):
    for agent in competingAgents:
        MoveAgent(agent, competingAgents, idleAgents)

    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] claimedTasks
    List[Agents] busyAgents
"""    
def Reassign(competingAgents, claimedTasks, busyAgents, idleAgents):
    for agent in competingAgents:
        for task in claimedTasks:
            if task.taskType == agent.skillType and agent.skillStrength < task.timeRequired:
                for agent2 in busyAgents:
                    if agent2.ID == task.assignedAgent:
                        weakerAgent = agent2
                MoveAgent(weakerAgent, busyAgents, idleAgents)
                MoveAgent(agent, competingAgents, busyAgents) 
                task.agentAssigned = agent.ID
                task.timeRequired = math.ceil(agent.skillStrength)


"""
"""     
def main(timeFactor, stagnationFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff):
    
    print("Hello")
    
    #start timers at 0
    timer = 0
    stagnationTimer = 0
    
    #create blackboard object
    blackboard = Blackboard(numTasks)

    #generate agents and tasks
    Initialization(blackboard, numAgents, numTasks, foxhedge, timeFactor)

    #start simulation loop
    while(numTasks != len(blackboard.completedTasks) and stagnationTimer < stagnationFactor):
        #assign unclaimed task
       # if(len())
        AssignUnclaimed(blackboard.idleAgents, blackboard.busyAgents, blackboard.unclaimedTasks, blackboard.claimedTasks, timeFactor)
        AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        timer = timer + 1 
        MakeCompetitors(blackboard.idleAgents, blackboard.competingAgents)
        random.shuffle(blackboard.unclaimedTasks)
        random.shuffle(blackboard.claimedTasks)
        Reassign(blackboard.competingAgents, blackboard.claimedTasks, blackboard.busyAgents, blackboard.idleAgents)
        RemoveCompetitors(blackboard.competingAgents, blackboard.idleAgents)
        AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        timer = timer + 1
        #print("timer =  : ", timer)
        #print("completed tasks", len(blackboard.completedTasks))
        print("stagnationTimer = ", stagnationTimer)
    
    #
    incompleteTasks = numTasks - len(blackboard.completedTasks)
    score = (scorecoeff * timer) - penalty * (incompleteTasks)
    print("Foxhedge ratio: ")
    print(foxhedge)
    print("Time: ")
    print(timer)
    print("Incomplete Tasks: ")
    print(incompleteTasks)
    print("Score: ")
    print(score)	
    


        
        
    
        
        


    
    
    
main(10, 5, 4, 20, 0.2, 0.1, 0.1)

