#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:25:00 2021

@author: carolineskalla
"""
import numpy as np
import matplotlib.pyplot as plt

import ATAFDSimulation
#from ATAFDSimulation import simulation

#Run simulation and collect more detailed results
def testSim(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff):
    
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
    blackboard = ATAFDSimulation.Blackboard(numTasks)
    #generate agents and tasks
    stagnationFactor = ATAFDSimulation.Initialization(blackboard, numAgents, numTasks, foxhedge, timeFactor)
    
    #copies for printing later
    agentList = list(blackboard.idleAgents)
    taskList = list(blackboard.unclaimedTasks)
    
    ATAFDSimulation.log("Agents:")
    for agent in agentList:
            ATAFDSimulation.log("agent ID: "+ str(agent.ID) + ", agent skillType: " + str(agent.skillType))
            
    ATAFDSimulation.log("\n")
    ATAFDSimulation.log("Tasks:")    
    for task in taskList:
            ATAFDSimulation.log("TaskID: "+ str(task.taskID) + ", task type: "+ str(task.taskType))
            
    ATAFDSimulation.log("\n")
    
    #are any tasks unsolvable     
    ATAFDSimulation.accessSkillTypes(blackboard.idleAgents, blackboard.unclaimedTasks)
    
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
        ATAFDSimulation.log("\n")
        ATAFDSimulation.log("While loop run:" + str(k))
        ATAFDSimulation.log("\n")
    
        
        #assign unclaimed tasks      
        ATAFDSimulation.AssignUnclaimed(blackboard.idleAgents, blackboard.busyAgents, blackboard.unclaimedTasks, blackboard.claimedTasks, timeFactor)
        
        #print detailed update:
        for task in blackboard.claimedTasks:
             ATAFDSimulation.log("Task ID: " + str(task.taskID) + ", type: " + str(task.taskType) + " Agent assigned (ID): " + str(task.agentAssigned.ID) + " Time Required: " + str(task.timeRequired))
        for task in blackboard.unclaimedTasks:
             ATAFDSimulation.log("Task ID: " + str(task.taskID) + ", type: " + str(task.taskType) + " Agent assigned (ID): " + str(task.agentAssigned.ID) + " Time Required: " + str(task.timeRequired))
         
       #agents do one time step of work on claimed tasks
        
        numTasksCompleted = ATAFDSimulation.AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        if numTasksCompleted == 0:
            stagnationTimer += 1
        elif numTasksCompleted > 0:
            stagnationTimer = 0
        
        
     
        

        """
        

        numTasksCompleted = AgentsWork(blackboard.busyAgents, blackboard.idleAgents, blackboard.claimedTasks, blackboard.completedTasks, stagnationTimer)
        if numTasksCompleted == 0:
            stagnationTimer += 1
        elif numTasksCompleted > 0:
            stagnationTimer = 0
        """

        ATAFDSimulation.log("completed " + str(len(blackboard.completedTasks)) + " out of " + str(numTasks)+ " tasks")
        ATAFDSimulation.log("stagnation timer: " + str(stagnationTimer))
        
       # print("stagnationTimer = ", stagnationTimer)
        timer += 1
        k = k + 1
        
        idleAgentsSize.append(len(blackboard.idleAgents))
        busyAgentsSize.append(len(blackboard.busyAgents))
        completedTasks.append(len(blackboard.completedTasks))
        unclaimedTasks.append(len(blackboard.unclaimedTasks))
        claimedTasks.append(len(blackboard.claimedTasks))
        time.append(k)
        
    ATAFDSimulation.log("\n")
    ATAFDSimulation.log("Parameters inputted:")
    ATAFDSimulation.log("time factor = " + str(timeFactor))
    ATAFDSimulation.log("stagnation factor = " + str(stagnationFactor))
    #log("stagnation factor = " + str(stagnationFactor))
    ATAFDSimulation.log("number of agents = " + str(numAgents))
    ATAFDSimulation.log("number of tasks = " + str(numTasks))
    ATAFDSimulation.log("foxhedge ratio = at least " + str(foxhedge*100) + " percent foxes") 
    #TODO: clarify in words what  penalty and score coefficient do
    ATAFDSimulation.log("penalty for incomplete tasks = " + str(penalty))
    ATAFDSimulation.log("score coefficient = " + str(scorecoeff))
    
    
    
    ATAFDSimulation.accessSkillTypes(agentList, taskList)
    
    #print("\n")
    #print("Simulation Results:")
    incompleteTasks = numTasks - len(blackboard.completedTasks)
    score = (scorecoeff * timer) + penalty * (incompleteTasks) 
    #print("Number of agents: " + str(numAgents) + "      % Fox: " + str(foxhedge) + "     % Hedgehog: " + str(1-foxhedge))
    #print("After working, agents complete "+ str(len(blackboard.completedTasks)) + " out of "+ str(numTasks)+ " tasks")
    #print("score: ", score)
    #print("Time taken: "+ str(timer))
    
    numUnclaimedTasks = len(blackboard.unclaimedTasks)
   
    
    return score, timer, numUnclaimedTasks ##, timer
   

                
                   

def test100A150T():
    scores = []
    times = []
    unclaimedTasks = []
   # scoreSet = set()
    numRuns= 100
    for i in range(numRuns):
        #print("Run: ", i)
        s, t, u = testSim(2, 100, 150, 0.8, 0.1, 0.1)
        #print(s)
        #s = 3
        scores.append(s)
        times.append(t)
        unclaimedTasks.append(u)
        print("Trial:", i, ",  Time:", times[i], ", # unclaimedTasks:", unclaimedTasks[i], ",  Score:", scores[i])
        
        
    #print(numRuns, " Runs")     
    # print("Scores:")
    # print(scores)
    # print("Unique scores: ", scoreSet)
    """            
    #plot scores vs trials
    trials = range(0, numRuns, 1)
    plt.figure()
    plt.scatter(trials, scores)
    plt.title('Score vs. Trial Run')
    plt.xlabel("trial #")
    plt.ylabel("Score")
    plt.figtext(.5, 0, "Proportion of Generalist = " + str(0.8) + " timeFactor = " + str(2) + ", numAgents = " + str(100) + ", numTasks = " + str(150) + ", penalty = " + str(0.1) +  ", scorecoeff = " + str(0.1) + ", numRuns = " + str(numRuns), ha="center", fontsize=9)
    plt.subplots_adjust(bottom=0.15)
    plt.show()
   """
test100A150T()   

