# -*- coding: utf-8 -*
"""
ATAFD version 1

Description: number of agents exist in the environment. The environment
generates a number of tasks, which the agents must solve. Tasks will be posted to the blackboard.
"""
import numpy as np

"""
Env class: Saves list of agents and maybe the lists of tasks
    attributes:
        list of all agents
        list of all tasks
 """

class Environment:
    def __init__(self, numTasks, numAgents, propFox, propHedge):
        self.numTasks = numTasks
        #create a list of all agents
        self.agentList = list()
        #create foxes (uniform ditribution of number of  skills)
        skillDist = np.random.randint(low = 2, high = 9, size = int(numAgents*propFox)
        for j in range(len(skillDist))                                      
            print(skillDist[j])
        for i in range(numAgents*propFox):
            self.agentList.append(Agent(skillDist[i], 1))           
        


"""
Agent class: 
    attributes:
        list of skill integers (0,1,2,3,4,5,6,7,8,9)
        skill strength = (1/ number of skill types) * 10
"""
class Agent:
    def _init_(self, numOfSkills, skillStrength ):
        #generate the skill
        self.skillSet = np.random.uniform(low=0, high=10, size=numOfSkills)
        self.skillStrength = skillStrength
        
"""
Task class:
    attributes:
        task type either 0,1,2,3,4,5,6,7,8,9
    
"""
        
"""
This function will control the steps in the simulation
"""
def simulate(numTasks, numAgents, propFox, propHedge):
    #initialization:
    environment = E2(numAgents)
    print(environment.numAgents)
    e1 = Environment(numTasks, numAgents, propFox, propHedge)
    print(e1.numTask)

    
"""
This function begins the simulation by calling the simulate() method
with the desired parameters. 
"""
def main():
    #begin simulation with chosen parameters
    simulate(100, 20, 0.5,0.5)
    #display the results in some way
main()
        
        