#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 20:58:41 2021

@author: carolineskalla
"""

def accessSkillTypes(idleAgents, unclaimedTasks):
    agentSkillTypes = set()
    taskSkillTypes = set()
    #collect all agent types
    for agent in idleAgents:
        skillSet = agent.skillType
        for skill in skillSet:
            agentSkillTypes.add(skill)
            
    for task in unclaimedTasks:
        taskSkillTypes.add(task)
        
    numSkillsMissing = taskSkillTypes  - agentSkillTypes 
    print(numSkillsMissing)
    
    
agentTypes = {3,4,5}
taskTypes = {1,2,3, 7}

print(taskTypes - agentTypes)

