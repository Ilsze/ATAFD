#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:25:00 2021

@author: carolineskalla
"""
import numpy as np
import matplotlib.pyplot as plt

from ATAFDSimulation import simulation

def test10A15T():
    scores = []
   # scoreSet = set()
    numRuns= 100
    for i in range(numRuns):
        print("Run: ", i)
        s = simulation(2, 100, 150, 0.8, 0.1, 0.1)
        #s = 3
        scores.append(s)
        #scoreSet.add(s)
        
    print(numRuns, " Runs")     
    print("Scores:")
    print(scores)
    # print("Unique scores: ", scoreSet)
                   
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
   
test10A15T()                   
                   