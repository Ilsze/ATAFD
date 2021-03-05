

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
    #debug change!
    numFox = int(math.ceil(numAgents*foxHedge))
    numHedge = numAgents - numFox
    log("numFox: "+ str(numFox))
    log("numHedge: "+ str(numHedge))
    
    #generate skill length for each fox with uniform distribution
    skillLength = np.random.randint(low = 2, high = 9, size = numFox)
    #create foxes
    for i in range(numFox):
        #create fox agents and append them to the list of idle agents 
        blackboard.idleAgents.append(Agent(i, skillLength[i]))
        
    for i in range(numHedge):
        #create hedgehog agents and append them to the list of idle agents 
        blackboard.idleAgents.append(Agent(i+numFox, 1))
        
    #shuffle list of agents
    #debug change!
    #blackboard.idleAgents = random.shuffle(blackboard.idleAgents)
    random.shuffle(blackboard.idleAgents)
    
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

"""
Note about Python lists: lists are dynamic, so when an element is deleted the indices of the other elements
will all be shifted. If we remove an agent from the list and move on to the next index we will skip the agent 
that was moved to fill the removed agent;s index. For this reason the index is only increased if an agent 
was not removed (a match was not found)

"""
def Assign(agentSource, busyAgents, taskSource, claimedTasks, timeFactor):
    #agents iterate through task list and take the first eligible match
    #agentIndex = 0
    #taskIndex = 0
    if agentSource is not None:
        for agent in list(agentSource):
        #for i in range(len(agentSource)):
            #agent = agentSource[agentIndex]
            if taskSource is not None:
                for task in list(taskSource):
                #for j in range(len(taskSource)):
                    #task = taskSource[j]
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
                    #if the types don;t match and this is the last task in the list, move on to next index
                   # elif  (j == len(taskSource)):
                        #agentIndex += 1
                        
               
                

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
    #debug change!
    numFinishedTasks = 0
    #agentIndex = 0
    #taskIndex = 0
    if claimedTasks is not None:
        #print("claimedTasks is not empty")
        for task in list(claimedTasks):
        #for i in range(len(claimedTasks)):
            #task = claimedTasks[taskIndex]
            
            #work on task by subtracting 1
            task.timeRequired = task.timeRequired - 1
            log("task updated timeRequired: "+ str(task.timeRequired))
            
            if task.timeRequired == 0:
                #move task from claimedTasks to completedTasks
                MoveTask(task, claimedTasks, completedTasks)
                #find the agent that was working on this task and move it to idle agents
                for agent in busyAgents:
                    if agent.ID == task.agentAssigned:
                        completer = agent
                MoveAgent(completer, busyAgents, idleAgents)
                
                #increase numFinishedTasks
                numFinishedTasks = numFinishedTasks + 1
        #if no tasks have been completed, increase stagnationTimer
            #else:
              # agentIndex += 1
               #taskIndex += 1
            
    log(str(numFinishedTasks) + " tasks were finished")
    return numFinishedTasks
    """
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] competingAgents
"""    
def MakeCompetitors(idleAgents, competingAgents):
   # agentIndex = 0
   # taskIndex = 0
    #print("inside makeCompetitors function:")
   # print("size of idleAgents: ", len(idleAgents))
    if idleAgents is not None:
    #for agent in idleAgents:
        #print("agent")
        #MoveAgent(agent, idleAgents, competingAgents)
        for i in range(len(idleAgents)):
            agent = idleAgents[0]
            MoveAgent(agent, idleAgents, competingAgents)
 
        
    #print("updated size idle agents ", len(idleAgents))
   # print("updated size competing agents ", len(competingAgents))

    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] idleAgents
"""    
def RemoveCompetitors(competingAgents, idleAgents):
    if idleAgents is not None:
        for i in range(len(competingAgents)):
            agent = competingAgents[0]
            MoveAgent(agent, competingAgents, idleAgents)

    
"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] claimedTasks
    List[Agents] busyAgents
"""    
def Reassign(competingAgents, claimedTasks, busyAgents, idleAgents):
    numTrades = 0
    #agentIndex = 0
    #taskIndex = 0
    if competingAgents is not None:
        for agent in list(competingAgents):
        #for i in range(len(competingAgents)):
            #agent = competingAgents[agentIndex]
            if claimedTasks is not None:
                for task in list(claimedTasks):
                #for j in range(len(claimedTasks)):
                    #task = claimedTasks[taskIndex]
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
                    #elif  (j == len(claimedTasks)):
                        #agentIndex += 1
    log("Number of trades made in the competition: "+ str(numTrades))
    
def accessSkillTypes(idleAgents, unclaimedTasks):
    agentSkillTypes = set()
    taskSkillTypes = set()
    #collect all agent types
    for agent in idleAgents:
        skillSet = agent.skillType
        for skill in skillSet:
            agentSkillTypes.add(skill)
            
    for task in unclaimedTasks:
        taskSkillTypes.add(task.taskType)
        
    numSkillsMissing = taskSkillTypes -  agentSkillTypes
    log("\n")
    log("Number of task types that cannot be solved by any agent: "+str(len(numSkillsMissing)))
    log("Task types are: "+ str(numSkillsMissing))
    #print("\n")
    #print("Number of task types that cannot be solved by any agent: "+str(len(numSkillsMissing)))
    #print("Task types are: "+ str(numSkillsMissing))
    
"""
"""     
def simulation(timeFactor, stagnationFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff):
    
    
    #start timers at 0
    timer = 0
    stagnationTimer = 0
    
    
    log("Beginning Simulation:")
    log("timer = "+ str(timer) )
    
    
    #create blackboard object
    blackboard = Blackboard(numTasks)
    log("stagnation timer = " + str(stagnationTimer))

    #generate agents and tasks
    Initialization(blackboard, numAgents, numTasks, foxhedge, timeFactor)
    
    log("Agents and tasks have been initialized: ")
    if blackboard.idleAgents is None:
        log("idleAgents is empty")
    else:
        log("Size of idleAgents list: " + str(len(blackboard.idleAgents)))
        for agent in blackboard.idleAgents:
            log("agent ID: "+ str(agent.ID) + ", agent skillType: " + str(agent.skillType))
           # print("agent skill type: ", agent.skillType)
            
    if blackboard.unclaimedTasks is None:
        log("unclaimedTasks is empty")
    else:    
        log("Size of unclaimedTasks list " + str(len(blackboard.unclaimedTasks)))
        for task in blackboard.unclaimedTasks:
            log("task taskType: " + str(task.taskType))
            
    accessSkillTypes(blackboard.idleAgents, blackboard.unclaimedTasks)
            
    

    

    #start simulation loop
    k = 1
    while(numTasks != len(blackboard.completedTasks) and stagnationTimer < stagnationFactor):
        log("While loop run:" + str(k))
        
        #assign unclaimed tasks      
        AssignUnclaimed(blackboard.idleAgents, blackboard.busyAgents, blackboard.unclaimedTasks, blackboard.claimedTasks, timeFactor)
        log("\n")
        log("Idle agents are assigned unclaimed tasks:")
        log("updated size of idleAgents: " + str(len(blackboard.idleAgents)))
        log("updated size of busyAgents: " + str(len(blackboard.busyAgents)))
        log("updated size of unclaimedTasks: " + str(len(blackboard.unclaimedTasks)))
        log("updated size of claimedTasks: " + str(len(blackboard.claimedTasks)))
        
        
        #agents do one time step of work on claimed tasks
        log("\n")
        log("Agents work on claimedTasks:")
        numTasksCompleted = AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        if numTasksCompleted == 0:
            stagnationTimer += 1
        elif numTasksCompleted > 0:
            stagnationTimer = 0
        log("stagnationTimer = " + str(stagnationTimer))
        #increase time
        #timer += 1
       
        """
            
        #temerarily move idleAgents to competingAgents
        log("\n") 
        log("Competing agents are generated:")
        log("old size of idleAgents: " + str(len(blackboard.idleAgents)))
        log("old size of competingAgents: " + str(len(blackboard.competingAgents)))
        MakeCompetitors(blackboard.idleAgents + blackboard.competingAgents)
        log("updated size of idleAgents: " + str(len(blackboard.idleAgents)))
        log("updated size of competingAgents: " + str(len(blackboard.competingAgents)))
        
        #randomize order of task lists
        random.shuffle(blackboard.unclaimedTasks)
        random.shuffle(blackboard.claimedTasks)
        
        #main competing function
        log("\n") 
        log("Agents compete for claimed tasks: ")
        log("old size of competingAgents: " + str(len(blackboard.competingAgents)))
        log("old size of busyAgents: " + str(len(blackboard.busyAgents)))
        log("old size of idleAgents: " + str(len(blackboard.idleAgents)))
        Reassign(blackboard.competingAgents, blackboard.claimedTasks, blackboard.busyAgents, blackboard.idleAgents)
        log("updated size of competingAgents: " + str(len(blackboard.competingAgents)))
        log("updated size of busyAgents: " + str(len(blackboard.busyAgents)))
        log("updated size of idleAgents: " + str(len(blackboard.idleAgents)))
        
        #move agents in competing list back to idle list
        log("\n") 
        log("Moving competingAgents back to idleAgents: ")
        log("old size of competingAgents: " + str(len(blackboard.competingAgents)))
        log("old size of idleAgents: " + str(len(blackboard.idleAgents)))
        RemoveCompetitors(blackboard.competingAgents, blackboard.idleAgents)
        log("updated size of competingAgents: " + str(len(blackboard.competingAgents)))
        log("updated size of idleAgents: " + str(len(blackboard.idleAgents)))
        
        #agents work again
        """
        """
        log("\n")
        log("Agents work on claimedTasks:")
        numTasksCompleted = AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        if numTasksCompleted == 0:
            stagnationTimer += 1
        log("stagnationTimer = " + str(stagnationTimer))
        """
        
        log("\n")
        log("End of loop iteration "+ str(k) + ":")
        
        log("timer: "+ str(timer))
        log("stagnationTimer: "+ str(stagnationTimer))
        log("completed " + str(len(blackboard.completedTasks)) + " out of " + str(numTasks)+ " tasks")
        log("**************************************")
       # print("stagnationTimer = ", stagnationTimer)
        timer += 1
        k = k + 1
    
    print("\n")
    print("Simulation Results:")
    incompleteTasks = numTasks - len(blackboard.completedTasks)
    score = (scorecoeff * timer) - penalty * (incompleteTasks) 
    print("Number of agents: " + str(numAgents) + "      % Fox: " + str(foxhedge) + "     % Hedgehog: " + str(1-foxhedge))
    print("Completed "+ str(len(blackboard.completedTasks)) + " out of "+ str(numTasks)+ " tasks")
    print("Time required: "+ str(timer))
    print("Score: " + str(score))
    
   #return 
   
    

        
        
    
        
        

"""
reminder
Parameters: 
    timeFactor, stagnationFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff
"""
   
#simulation(10, 2000, 100, 1000, .2, 0.1, 0.1)
#simulation(10, 3, 4, 10, .2, 0.1, 0.1)

def main():
       simulation(10, 3, 4, 1, 0.2, 0.1, 0.1) 
       #simulation(10, 2000, 100, 1000, .2, 0.1, 0.1) 
       #simulation(10, 2000, 100, 1000, .4, 0.1, 0.1) 
       #simulation(10, 2000, 100, 1000, .6, 0.1, 0.1) 
       #simulation(10, 2000, 100, 1000, .8, 0.1, 0.1)
    
main()