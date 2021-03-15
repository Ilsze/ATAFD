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

class Agent:
    def __init__(self, ID, skill1, skill2, skill3, skill4, skill5):
        self.ID = ID      
        self.skillType = set()
        self.skillType.add(skill1)
        self.skillType.add(skill2)
        self.skillType.add(skill3)
        self.skillType.add(skill4)
        self.skillType.add(skill5)
        self.skillLength = len(self.skillType)
       
       
       
                
    
"""
Tasks:
    attributes (Type Name): Integer taskType, Integer agentAssigned, Float timeRequired, Float pendingTimerequired
"""

class Task:
     def __init__(self, taskID, taskType):
         #task types tange from 0 to 9
        self.taskType = taskType
        self.taskID = taskID
        #set to blank Agent when no agent is assigned
        self.agentAssigned = Agent(-1, -1, -1, -1, -1, -1)
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


def Initialization(blackboard, numAgents, numTasks, foxHedge, timeFactor):
    
    
    #determine number of foxes and hedges from foxhedge ratio
    #if the foxhedge ratio doesn't divide numAgents cleanly, round up the number of foxes
    #debug change!
    numFox = int(math.ceil(numAgents*foxHedge))
    numHedge = numAgents - numFox
    log("numFox: "+ str(numFox))
    log("numHedge: "+ str(numHedge))
    
    #generate skill length for each fox with uniform distribution
    skillLength = np.random.randint(low = 3, high = 11, size = numFox)
    maxSkillLength = max(skillLength)
    stagnationFactor = maxSkillLength * timeFactor
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
        blackboard.unclaimedTasks.append(Task(i))
        
    
    return stagnationFactor    

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



def main():
	#parameters
	numTasks = 5
	competingAgents = []
	idleAgents = []
	unclaimedTasks = []
	claimedTasks = []
	busyAgents = []
	timeFactor = 1
	agentsAssignedToTasks = []

	#create list contents
	competingAgents.append(Agent(0, 0, 0, 0, 0, 1)) ##this agent has skillLength 2
	competingAgents.append(Agent(1, 0, 0, 0, 0, 0)) ##this agent has skillLength 1
	#competingAgents.append(Agent(3, 0, 0, 0, 0, 0)) ##this agent has skillLength 1
	#competingAgents.append(Agent(4, 0, 0, 0, 0, 1)) ##this agent has skillLength 2
	idleAgents.append(Agent(2, 0, 1, 2, 3, 4))
	unclaimedTasks.append(Task(1, 0))
	Assign(idleAgents, busyAgents, unclaimedTasks, claimedTasks, timeFactor)

	for agent in list(competingAgents):
		print("Competing agent ID: " + str(agent.ID) + ". skillset: " + str(agent.skillType))

	for agent in list(busyAgents):
		print("Busy agent ID: " + str(agent.ID) + ". skillset: " + str(agent.skillType))

	for task in list(claimedTasks):
		print("task ID: " + str(task.taskID) + ". taskType: " + str(task.taskType) + ". timeRequired: " + str(task.timeRequired) + ". agentAssigned: " + str(task.agentAssigned.ID))


	Reassign(competingAgents, claimedTasks, busyAgents, idleAgents, timeFactor)


main()

#Reassign works for handover from 1 agent to another