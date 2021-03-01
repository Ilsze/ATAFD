#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 00:29:34 2021

@author: carolineskalla
"""

        

def MoveAgent(toBeMoved, source, destination): 
    #remove agent from source list
    #source.remove(toBeMoved)
    toBeMoved = source.pop()
    print("\n")
    print(source)

    #add agent to destination list
    destination.append(toBeMoved)
    print(destination)
    
  
idleAgents = [1,1,1]
competingAgents = []

print("initial idleAgents size: ", len(idleAgents))
print("initial competingAgents size: ", len(competingAgents))

print("idleAgents: ", idleAgents)
print("competingAgents: ", competingAgents)

for agent in idleAgents:
#for i in range(len(idleAgents)):
    #agent = idleAgents.pop()
    MoveAgent(agent, idleAgents, competingAgents)
        
        
        
print("new idleAgents size: ", len(idleAgents))
print("new competingAgents size: ", len(competingAgents))       
