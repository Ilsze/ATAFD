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
from statistics import mean 

#To use debugging print statements set DEBUG to True
DEBUG = True

def log(s):
    if DEBUG:
        print(s)



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
            #skill types range from 0 to 9
            self.skillType.add(randint(0, 9))
            length =  len(self.skillType)
       
                
    
"""
Tasks:
    attributes (Type Name): Integer taskType, Integer agentAssigned, Float timeRequired, Float pendingTimerequired
"""

class Task:
     def __init__(self, taskID):
         #task types tange from 0 to 9
        self.taskType = randint(0, 9)
        self.taskID = taskID
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
    #if the foxhedge ratio doesn't divide numAgents cleanly, round up the number of foxe
    numFox = int(math.ceil(numAgents*foxHedge))
    numHedge = numAgents - numFox
    
    
    #generate skill length for each fox with uniform distribution
    skillLength = np.random.randint(low = 3, high = 11, size = numFox)
    maxSkillLength = max(skillLength)
    #stagnationFactor is the longest skill length multiplied by the time factor (the longest length of time it should take any agent to solve a task)
    stagnationFactor = maxSkillLength * timeFactor
    #create foxes
    for i in range(numFox):
        #create fox agents and append them to the list of idle agents 
        blackboard.idleAgents.append(Agent(i, skillLength[i]))
        
    for i in range(numHedge):
        #create hedgehog agents and append them to the list of idle agents 
        blackboard.idleAgents.append(Agent(i+numFox, 1))
        
    #shuffle list of agents
    random.shuffle(blackboard.idleAgents)
    
    #generate tasks
    for i in range(numTasks):
        blackboard.unclaimedTasks.append(Task(i))
        
    
    return stagnationFactor    
   
        
    
    
       


"""
MoveTask:
Paramters (Type Name): 
    Task toBeMoved - task to me moved
    List[Task] source - list it's being moved from
    List[Task] destination - list it's being moved to
"""   
def MoveTask(toBeMoved, source, destination): 
    if toBeMoved in source:
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
    if toBeMoved in source:
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

"""
Note about Python lists: lists are dynamic, so when an element is deleted the indices of the other elements
will all be shifted. If we remove an agent from the list and move on to the next index we will skip the agent 
that was moved to fill the removed agent;s index. For this reason the index is only increased if an agent 
was not removed (a match was not found)

"""
def Assign(agentSource, busyAgents, taskSource, claimedTasks, timeFactor):
    #agents iterate through task list and take the first eligible match

    if agentSource is not None:
        for agent in list(agentSource):
            if taskSource is not None:
                for task in list(taskSource):
                    #if task type matches agent type
                    if task.taskType in agent.skillType:
                        #update necessary info
                        task.agentAssigned = agent.ID
                        task.timeRequired = timeFactor*agent.skillLength
                        #move the task to claimed tasks
                        MoveTask(task, taskSource, claimedTasks)
                        #move the agent to busy agents
                        MoveAgent(agent, agentSource, busyAgents)
                        #after first match is found, break tasks loop and go to next agent 
                        break
                        
               
                

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
Agents Work: For each task in the claimed task list, the time required to complete is deacreased by 1.
If the time required is 0 , the task is moved to the complete task list 
"""     
def AgentsWork(busyAgents, idleAgents, claimedTasks, completedTasks, stagnationTimer):
    numFinishedTasks = 0
    
    if claimedTasks is not None:
        #print("claimedTasks is not empty")
        for task in list(claimedTasks):
            task.timeRequired = task.timeRequired - 1

            if task.timeRequired <= 0:
                #move task from claimedTasks to completedTasks
                MoveTask(task, claimedTasks, completedTasks)
                #find the agent that was working on this task and move it to idle agents
                for agent in busyAgents:
                    if agent.ID == task.agentAssigned:
                        completer = agent
                MoveAgent(completer, busyAgents, idleAgents)
                
                #increase numFinishedTasks
                numFinishedTasks = numFinishedTasks + 1
            
  
    return numFinishedTasks
    """
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] competingAgents
"""    
def MakeCompetitors(idleAgents, competingAgents):
    if idleAgents is not None:
        for agent in list(idleAgents):

            MoveAgent(agent, idleAgents, competingAgents)
 

    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] idleAgents
"""    
def RemoveCompetitors(competingAgents, idleAgents):
    if idleAgents is not None:
        for agent in list(competingAgents):
            
            MoveAgent(agent, competingAgents, idleAgents)

    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] claimedTasks
    List[Agents] busyAgents
"""    
def Reassign(competingAgents, claimedTasks, busyAgents, idleAgents):
    numTrades = 0
    
    if competingAgents is not None:
        for agent in list(competingAgents):

            if claimedTasks is not None:
                for task in list(claimedTasks):
                    if task.taskType == agent.skillType and agent.skillStrength < task.timeRequired:
                        #if competing agent is better, search the list for weaker agent
                        for agent2 in busyAgents:
                            if agent2.ID == task.assignedAgent:
                                weakerAgent = agent2
                                
                        MoveAgent(weakerAgent, busyAgents, idleAgents)
                        MoveAgent(agent, competingAgents, busyAgents) 
                        task.agentAssigned = agent.ID
                        task.timeRequired = math.ceil(agent.skillStrength)
                        numTrades += 1
                        break                           
    
def accessSkillTypes(idleAgents, unclaimedTasks):
    agentSkillTypes = set()
    taskSkillTypes = set()
    numTasksUnsolvable = 0
    unsolvableTasks = set()
    
    #collect all agent types
    for agent in idleAgents:
        skillSet = agent.skillType
        for skill in skillSet:
            agentSkillTypes.add(skill)
            
    for task in unclaimedTasks:
        taskSkillTypes.add(task.taskType)
        if task.taskType not in agentSkillTypes:
           numTasksUnsolvable += 1
           unsolvableTasks.add(task)

        
    #skillsMissing = taskSkillTypes -  agentSkillTypes
   
    if unsolvableTasks is None:
        log("All tasks are solvable")
    else:
        for task in unsolvableTasks:
            log(str(numTasksUnsolvable) + " unsolvable tasks:")
            log("Task ID: " + str(task.taskID) + ", Type: " + str(task.taskType))
  
"""
"""     
def simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff):
    
    #for plotting agent lists
    idleAgentsSize = []
    busyAgentsSize = []
    completedTasks = []
    unclaimedTasks = []
    claimedTasks = []
    time = []
    
    #start timers at 0
    timer = 0
    stagnationTimer = 0
    
    
    #create blackboard object
    blackboard = Blackboard(numTasks)
    #generate agents and tasks
    stagnationFactor = Initialization(blackboard, numAgents, numTasks, foxhedge, timeFactor)
    
    #copies for printing later
    agentList = list(blackboard.idleAgents)
    taskList = list(blackboard.unclaimedTasks)
    
    log("Agents:")
    for agent in agentList:
            log("agent ID: "+ str(agent.ID) + ", agent skillType: " + str(agent.skillType))
            
    log("\n")
    log("Tasks:")    
    for task in taskList:
            log("TaskID: "+ str(task.taskID) + ", task type: "+ str(task.taskType))
            
    log("\n")
    
    #are any tasks unsolvable     
    accessSkillTypes(blackboard.idleAgents, blackboard.unclaimedTasks)
    
    #for plots (initial sizes)
    idleAgentsSize.append(len(blackboard.idleAgents))
    busyAgentsSize.append(len(blackboard.busyAgents))
    completedTasks.append(len(blackboard.completedTasks))
    unclaimedTasks.append(len(blackboard.unclaimedTasks))
    claimedTasks.append(len(blackboard.claimedTasks))
    time.append(0)
    
    #start simulation loop
    k = 1
    #stagnationTimer < stagnationFactor
    while(numTasks != len(blackboard.completedTasks) and stagnationTimer < stagnationFactor):
        log("\n")
        log("While loop run:" + str(k))
        log("\n")
    
        
        #assign unclaimed tasks      
        AssignUnclaimed(blackboard.idleAgents, blackboard.busyAgents, blackboard.unclaimedTasks, blackboard.claimedTasks, timeFactor)
        
        #print detailed update:
        for task in blackboard.claimedTasks:
            log("Task ID: " + str(task.taskID) + ", type: " + str(task.taskType) + " Agent assigned (ID): " + str(task.agentAssigned) + " Time Required: " + str(task.timeRequired))
        for task in blackboard.unclaimedTasks:
             log("Task ID: " + str(task.taskID) + ", type: " + str(task.taskType) + " Agent assigned (ID): " + str(task.agentAssigned) + " Time Required: " + str(task.timeRequired))
         
       #agents do one time step of work on claimed tasks
        
        numTasksCompleted = AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        if numTasksCompleted == 0:
            stagnationTimer += 1
        elif numTasksCompleted > 0:
            stagnationTimer = 0
        
        #increase time
        #timer += 1
       
      
            
        #temerarily move idleAgents to competingAgents
     
       # MakeCompetitors(blackboard.idleAgents, blackboard.competingAgents)
       
        
        
        #randomize order of task lists
        #random.shuffle(blackboard.unclaimedTasks)
        #random.shuffle(blackboard.claimedTasks)
        
        #main competing function
        #Reassign(blackboard.competingAgents, blackboard.claimedTasks, blackboard.busyAgents, blackboard.idleAgents)

        #move agents in competing list back to idle list
       # RemoveCompetitors(blackboard.competingAgents, blackboard.idleAgents)
        
        #agents work again
        """
        

        numTasksCompleted = AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        if numTasksCompleted == 0:
            stagnationTimer += 1
        elif numTasksCompleted > 0:
            stagnationTimer = 0
        """

        log("completed " + str(len(blackboard.completedTasks)) + " out of " + str(numTasks)+ " tasks")
        log("stagnation timer: " + str(stagnationTimer))
        
       # print("stagnationTimer = ", stagnationTimer)
        timer += 1
        k = k + 1
        
        idleAgentsSize.append(len(blackboard.idleAgents))
        busyAgentsSize.append(len(blackboard.busyAgents))
        completedTasks.append(len(blackboard.completedTasks))
        unclaimedTasks.append(len(blackboard.unclaimedTasks))
        claimedTasks.append(len(blackboard.claimedTasks))
        time.append(k)
        
    log("\n")
    log("Parameters inputted:")
    log("time factor = " + str(timeFactor))
    log("stagnation factor = " + str(stagnationFactor))
    #log("stagnation factor = " + str(stagnationFactor))
    log("number of agents = " + str(numAgents))
    log("number of tasks = " + str(numTasks))
    log("foxhedge ratio = at least " + str(foxhedge*100) + " percent foxes") 
    #TODO: clarify in words what  penalty and score coefficient do
    log("penalty for incomplete tasks = " + str(penalty))
    log("score coefficient = " + str(scorecoeff))
    
    
    
    accessSkillTypes(agentList, taskList)
    
    print("\n")
    print("Simulation Results:")
    incompleteTasks = numTasks - len(blackboard.completedTasks)
    score = (scorecoeff * timer) + penalty * (incompleteTasks) 
    print("Number of agents: " + str(numAgents) + "      % Fox: " + str(foxhedge) + "     % Hedgehog: " + str(1-foxhedge))
    print("Completed "+ str(len(blackboard.completedTasks)) + " out of "+ str(numTasks)+ " tasks")
    print("score: ", score)
    print("Time taken: "+ str(timer))
    

    plt.figure(1)
    plt.plot(time, idleAgentsSize, label = "idleAgents")
    plt.plot(time, busyAgentsSize, label = "busyAgents")
    #plt.plot(time, unclaimedTasks, label = "unclaimedTasks")
    #plt.plot(time, claimedTasks, label = "claimedTasks")
    plt.xlabel('Time')
    plt.ylabel('Number of agents/tasks')
    plt.legend()
    
    plt.figure(2)
    plt.plot(time, completedTasks, label = "completedTasks")
    plt.xlabel('Time')
    plt.ylabel('Number of completed tasks')
   
    
    return [score, timer]
   
    

        
        
    
        
        

"""
reminder
Parameters: 
    timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff
"""
   
#simulation(10, 2000, 100, 1000, .2, 0.1, 0.1)
#simulation(10, 3, 4, 10, .2, 0.1, 0.1)

def main():
    
       import sys
       sys.stdout=open("test3.txt","w")

       


       simulation(1, 10, 15, 0.2, 0.1, 0.1) 
       """
       #simulation(10, 100, 1000, .1, 0.1, 0.1)
       simulation(10, 100, 1000, .2, 0.1, 0.1)
       #simulation(10, 100, 1000, .3, 0.1, 0.1)
       simulation(10, 100, 1000, .2, 0.1, 0.1)
       #simulation(10, 100, 1000, .5, 0.1, 0.1)
       simulation(10, 100, 1000, .6, 0.1, 0.1) 
       #simulation(10, 100, 1000, .7, 0.1, 0.1)
       simulation(10, 100, 1000, .8, 0.1, 0.1)
       """
       
       sys.stdout.close()
       
       
       
     
       
    
main()
    
