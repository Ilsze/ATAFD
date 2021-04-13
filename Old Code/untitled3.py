#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:25:00 2021

@author: carolineskalla
"""

def test10A15T():
    scores = []
   # scoreSet = set()
    numRuns= 100
    for i in range(numRuns):
        print("Run: ", i)
        s = simulation(2, 10, 15, 0.8, 0.1, 0.1)
        scores.append(s)
        #scoreSet.add(s)
        
    print(numRuns, " Runs")     
    print("Scores:")
    print(scores)
   # print("Unique scores: ", scoreSet)
                   
#test10A15T()                   
                   