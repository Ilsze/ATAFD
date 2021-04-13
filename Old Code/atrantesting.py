#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 00:29:34 2021

@author: carolineskalla
"""

        

def MoveAgent(toBeMoved, source, destination): 
    #remove agent from source list
    source.remove(toBeMoved)
    #toBeMoved = source.pop()
    #print("\n")
    #print(source)

    #add agent to destination list
    destination.append(toBeMoved)
  #  print(destination)
    
#sometimes delete
  
idleAgents = [1,2,3, 4, 5, 6, 7, 8, 9]
competingAgents = []

print("initial idleAgents size: ", len(idleAgents))
print("initial competingAgents size: ", len(competingAgents))

print("idleAgents: ", idleAgents)
print("competingAgents: ", competingAgents)

#for agent in idleAgents:
index = 0
for i in range(len(idleAgents)):
    agent = idleAgents[index]
    print("agent: ", agent)
    if i % 3 == 0:
        MoveAgent(agent, idleAgents, competingAgents)
    else:
        index += 1
        
        
        
print("new idleAgents size: ", len(idleAgents))
print("new competingAgents size: ", len(competingAgents))  

print("new idleAgents: ", idleAgents)
print("new competingAgents: ", competingAgents)   

#always delete
idleAgents2 = [1,2,3, 4, 5, 6, 7, 8, 9]
competingAgents2 = []

print("initial idleAgents2 size: ", len(idleAgents2))
print("initial competingAgents2 size: ", len(competingAgents2))

print("idleAgents2: ", idleAgents2)
print("competingAgents2: ", competingAgents2)

#for agent in idleAgents:
#index = 0
for i in range(len(idleAgents2)):
    agent = idleAgents2[0]
    print("agent: ", agent)
    #if i % 3 == 0:
    MoveAgent(agent, idleAgents2, competingAgents2)
    
        
        
        
print("new idleAgents2 size: ", len(idleAgents2))
print("new competingAgents2 size: ", len(competingAgents2))  

print("new idleAgents2: ", idleAgents2)
print("new competingAgents2: ", competingAgents2) 
  
