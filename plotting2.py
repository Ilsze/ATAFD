#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 23:23:51 2021

@author: carolineskalla
"""

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
import statistics
from mpl_toolkits import mplot3d
#To use debugging print statements set DEBUG to True
DEBUG = False

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
    attributes (Type Name): Integer taskType, Agent agentAssigned, Float timeRequired, Float pendingTimerequired
"""

class Task:
     def __init__(self, taskID):
         #task types tange from 0 to 9
        self.taskType = randint(0, 9)
        self.taskID = taskID
        #set to blank Agent when no agent is assigned
        self.agentAssigned = Agent(-1, 0)
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
                        task.agentAssigned = agent
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
                    if agent == task.agentAssigned:
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
    List[Agents] competingAgents
    List[Tasks]  claimedTasks
    List[Agents] busyAgents
    List[Agents] idleAgents
    Integer      timeFactor
"""    
def Reassign(competingAgents, claimedTasks, busyAgents, idleAgents, timeFactor):
    numTrades = 0
    if claimedTasks is not None:
        log("iterating through list of claimedtasks...")
        for task in list(claimedTasks):
            for competingAgent in list(competingAgents):
                #if competing agent is better than agent assigned, reassign claimed task
                if task.taskType in competingAgent.skillType and (competingAgent.skillLength * timeFactor) < task.timeRequired:
                    log("agent " + str(competingAgent.ID) + " takes task from agent " + str(task.agentAssigned.ID))
                    #move weaker agent into idleAgents and strongerAgent into busyAgents
                    MoveAgent(task.agentAssigned, busyAgents, idleAgents)
                    MoveAgent(competingAgent, competingAgents, busyAgents)
                    task.agentAssigned = competingAgent
                    task.timeRequired = competingAgent.skillLength * timeFactor
                    numTrades += 1
                    break
    log("Number of trades made in the competition: " + str(numTrades))                         


"""
Parameters (Type Name):
    List[Agents] idleAgents
    List[Tasks]  unclaimedTasks
"""
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
             log("Task ID: " + str(task.taskID) + ", type: " + str(task.taskType) + " Agent assigned (ID): " + str(task.agentAssigned.ID) + " Time Required: " + str(task.timeRequired))
        for task in blackboard.unclaimedTasks:
             log("Task ID: " + str(task.taskID) + ", type: " + str(task.taskType) + " Agent assigned (ID): " + str(task.agentAssigned.ID) + " Time Required: " + str(task.timeRequired))
         
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
        #Reassign(blackboard.competingAgents, blackboard.claimedTasks, blackboard.busyAgents, blackboard.idleAgents, timeFactor)

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
    print("After working, agents complete "+ str(len(blackboard.completedTasks)) + " out of "+ str(numTasks)+ " tasks")
    print("score: ", score)
    print("Time taken: "+ str(timer))
    

#Plots Agents/Tasks vs Time and Number completed tasks vs time (for 1 simulation run)
     #Would like turn this into a function
     
    """
    plt.figure(1)
    plt.plot(time, idleAgentsSize, label = "idleAgents")
    plt.plot(time, busyAgentsSize, label = "busyAgents")
    #plt.plot(time, unclaimedTasks, label = "unclaimedTasks")
    #plt.plot(time, claimedTasks, label = "claimedTasks")
    plt.title('Number of Agents vs. Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Agents')
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.32, 1.025), fancybox=True)
    #plt.legend()
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff), ha="center", fontsize=9) 
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    """
    """
    plt.figure(2)
    plt.plot(time, completedTasks, label = "completedTasks")
    plt.title('Number of Completed Tasks vs. Time')
    plt.xlabel('Time')
    plt.ylabel('Number of completed tasks')
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff), ha="center", fontsize=9) 
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    """
   
    
    return score ##, timer
   
    
def plotScores(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList):
    meanScores = []
    medianScores = []
    
    #find the mean and median of each sublist
    j = 0
    while(j < len(masterScoreList)):
    	meanScores.append(statistics.mean(masterScoreList[j]))
    	medianScores.append(statistics.median(masterScoreList[j]))
    	j += 1

    #print(str(simulation(1, 10, 15, 0.2, 0.1, 0.1)))
    print("foxhedge array:")
    print(foxhedgeArray)
    print('MasterScoreList:')
    print(masterScoreList)
    print('meanScores: ')
    print(meanScores)
    
    #Mean score vs fox ratio (for multiple runs)
    plt.figure(3)
    x = np.array(foxhedgeArray)
    plt.scatter(x, meanScores)
    m, b = np.polyfit(x, medianScores, 1)
    plt.plot(x, m*x + b)
    plt.title('Mean Scores vs. Proportion of Generalists')
    plt.xlabel("Proportion of Generalists")
    plt.ylabel("Mean Scores")
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numTrials), ha="center", fontsize=9)
    plt.subplots_adjust(bottom=0.15)
    plt.show()

    #Median score  vs fox ratio (for multiple runs)
    plt.figure(4)
    x = np.array(foxhedgeArray)
    plt.scatter(x, medianScores)
    m, b = np.polyfit(x, medianScores, 1)
    plt.plot(x, m*x + b)
   # plt.plot(foxhedgeArray, np.poly1d(np.polyfit(foxhedgeArray, medianScores, 1)*foxhedgeArray)
    plt.title('Median Scores vs. Proportion of Generalists')
    plt.xlabel("Proportion of Generalists")
    plt.ylabel("Median Scores")
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numTrials), ha="center", fontsize=9) 
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    
    #All score points vs fox ratio (for multiple runs)

    plt.figure(3)
    x = np.array(foxhedgeArray)
    for n in range(len(masterScoreList[0])):
        y = []
        for l in masterScoreList:
            y.append(l[n])
        plt.scatter(x, y, label = "Run: " + str(n+1))
        #plt.scatter(x, y)
       # m, b = np.polyfit(x, y, 1)
       # plt.plot(x, m*x + b)
    
    plt.title('Score vs. Proportion of Generalists')
    plt.xlabel("Proportion of Generalists")
    plt.ylabel("Score")
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.25, 1.025), fancybox=True)
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numTrials), ha="center", fontsize=9)
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    
   
def plotScoreTimeFactor(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, timeFactorArray, masterScoreList2):
    plt.figure(4)
    x = np.array(timeFactorArray)
    for n in range(len(masterScoreList2[0])):
       y = []
       for r in masterScoreList2:
            y.append(r[n])
       plt.scatter(x, y, label = '= ' + str(foxhedgeArray[n]))
       m, b = np.polyfit(x, y, 1)
       plt.plot(x, m*x + b)
    
    plt.title('Score vs. timeFactor')
    plt.xlabel("timeFactor")
    plt.ylabel("Score")
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.42, 1.025), fancybox=True, title = 'Proportion of Generalists')
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numTrials), ha="center", fontsize=9)
    plt.subplots_adjust(bottom=0.15)
    plt.show()        
        
    
#plots score as number of agents and proportion of generalist are varied
def plot3DAgentsNum():
    print()
    
        
        

"""
reminder
Parameters: 
    timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff
"""
   
#simulation(10, 2000, 100, 1000, .2, 0.1, 0.1)
#simulation(10, 3, 4, 10, .2, 0.1, 0.1)

def main():
    
    #Plots for mean and median score vs time (over multiple trials)
    
    import sys
   # sys.stdout=open("test3.txt","w")
    """
    #user sets foxhedge ratios she's interested in using foxhedgeArray])
    foxhedgeArray = ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    foxhedgeArraySize = len(foxhedgeArray)
    masterScoreList = []
  
    #generate as many lists as there are foxhedge ratios
    i = 0
    while(i < foxhedgeArraySize):
    	temp = []
    	masterScoreList.append(temp)
    	i += 1

    #fill in sublists of masterScoreList. Each contains scores from one foxhedge ratio
    numRuns = 2
    numTrials = numRuns
    while(numRuns > 0):
        index = 0
        for ratio in foxhedgeArray:
            #timeFactor = 2, 10 agents, 15 tasks, ratio
            timeFactor = 2
            numAgents = 5
            numTasks = 15
            foxhedge = ratio
            penalty = 0.1 
            scorecoeff = 0.1
            score = simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff)
            masterScoreList[index].append(score)
            index += 1
        numRuns -= 1
        
    plotScores(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList)
"""
"""
#def testTimeFactor():
   #testing time factor
    numRuns = 100
    masterScoreList2 = []
    timeFactorArray = [1,2,3,4,5,6,7,8,9,10]
    #generate as many lists as there are foxhedge ratios
    i = 0
    while(i < len(timeFactorArray)):
    	temp = []
    	masterScoreList2.append(temp)
    	i += 1
        
    index = 0   
    for tf in timeFactorArray:
        for ratio in foxhedgeArray:
            trialScores = []
            for run in range(numRuns):
                timeFactor = tf
                numAgents = 100
                numTasks = 150
                foxhedge = ratio
                penalty = 0.1 
                scorecoeff = 0.1
                score = simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff)
                trialScores.append(score)
                
            avg = statistics.mean(trialScores)
            masterScoreList2[index].append(avg)
            
        index += 1
    plotScoreTimeFactor(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numRuns, foxhedgeArray, timeFactorArray, masterScoreList2)
     """         
    

    

"""
    #fill in sublists of masterScoreList. Each contains scores from one foxhedge ratio
    numRuns = 5
    numTrials = numRuns
    while(numRuns > 0):
        index = 0
        for tf in timefactorArray:
            #timeFactor = 2, 10 agents, 15 tasks, ratio
            timeFactor = tf
            numAgents = 10
            numTasks = 15
            foxhedge = ratio
            penalty = 0.1 
            scorecoeff = 0.1
            score = simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff)
            masterScoreList[index].append(score)
            index += 1
        numRuns -= 1
        
    plotScores(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList) 
    """
#testTimeFactor()
       
def Test3D():
    #3D plot of the number of agents and the prortion of generalists
    numRuns = 100
    masterScoreList3D = []
    #vary proportion of generalists
    foxhedgeArray = ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    foxhedgeArraySize = len(foxhedgeArray)
    #vary number of agents
    agentNumbers = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 500, 1000])
    #numTasks = 10*numAgents
    i = 0
    while(i < foxhedgeArraySize):
    	temp = []
    	masterScoreList3D.append(temp)
    	i += 1
        
    #print(numAgents)
    #print(numTasks)
    index = 0
    for ratio in foxhedgeArray:
        for agentNum in agentNumbers:
            for runs in range(numRuns):
                trials = []
                timeFactor = 2
                numAgents = agentNum
                numTasks = agentNum*10
                foxhedge = ratio
                penalty = 0.1 
                scorecoeff = 0.1
                score = simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff)
                trials.append(score)
            avg = statistics.mean(trials)
            masterScoreList3D[index].append(avg)
        index += 1
        
    #plotting 3D
    x = []
    y = []
    z = []
    count = 0
    for r in masterScoreList3D:
        count2 = 0
        for na in r:
            x.append(foxhedgeArray[count])
            y.append(agentNumbers[count2])
            z.append(na)
            count2 += 1
        count += 1
            
       
    # Creating figure
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
         
    # Creating plot
    ax.scatter3D(x, y, z, color = "blue")
    plt.title("Mean Score vs Number of Agents and Proportion of Generalists")
    plt.xlabel('Proportion of Generalists')
    plt.ylabel('Number of Agents')
    ax.set_zlabel('Mean Score')
    plt.figtext(.5, 0.07, "timeFactor = " + str(timeFactor) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numRuns), ha="center", fontsize=10)
 
    # show plot
    plt.show()
                
    
    
Test3D()
   # sys.stdout.close()
#main()