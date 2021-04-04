#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun 4th April 2021

@author: carolineskalla and jojolee
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This file generates 2D plots based on code in plotting2

"""

#General imports
import numpy as np
import matplotlib.pyplot as plt
import random
from random import randint
import math
import statistics
import sys
from mpl_toolkits import mplot3d
#import seaborn as sns
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import griddata

#plotting2 imports
from plotting2 import log
from plotting2 import Agent
from plotting2 import Task
from plotting2 import Blackboard
from plotting2 import Initialization
from plotting2 import MoveTask
from plotting2 import MoveAgent
from plotting2 import Assign
from plotting2 import AssignUnclaimed
from plotting2 import AgentsWork
from plotting2 import accessSkillTypes
from plotting2 import simulation
from plotting2 import Test3D


#this function does 2D mean and median plots (score vs foxhedge ratio)
def meanScoreVsFoxhedge(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList):
    sys.stdout=open("2Dmean.txt","w")

    meanScores = []

    #find the mean of each sublist
    j = 0
    while(j < len(masterScoreList)):
        meanScores.append(statistics.mean(masterScoreList[j]))
        j += 1

    #Mean score vs fox ratio (for multiple runs)
    plt.figure(1)
    x = np.array(foxhedgeArray)
    plt.scatter(x, meanScores)
    m, b = np.polyfit(x, meanScores, 1)
    plt.plot(x, m*x + b)
    plt.title('Mean Scores vs. Proportion of Generalists')
    plt.xlabel("Proportion of Generalists")
    plt.ylabel("Mean Scores")
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numTrials), ha="center", fontsize=9)
    plt.subplots_adjust(bottom=0.15)
    plt.show()

    sys.stdout.close()



def medianScoreVsFoxhedge(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList):
    sys.stdout=open("2Dmedian.txt","w")

    medianScores = []

    #find the median of each sublist
    j = 0
    while(j < len(masterScoreList)):
        medianScores.append(statistics.median(masterScoreList[j]))
        j += 1
    
    #Median score  vs fox ratio (for multiple runs)
    plt.figure(2)
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

    sys.stdout.close()
    


def allScoreVsFoxhedge(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList):
    sys.stdout=open("2DallScore.txt","w")

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

    sys.stdout.close()




def plotScoreVsTimeFactor(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, timeFactorArray, masterScoreList2):
    sys.stdout=open("2DAllScore.txt","w")
    print("hello")

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

    sys.stdout.close()     
    


def graph2D():
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
    numRuns = 100
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
    
    #comment the following code in or out to generate the desired plots
    meanScoreVsFoxhedge(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList)
    medianScoreVsFoxhedge(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList)
    allScoreVsFoxhedge(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList)



def graphScoreVsTimeFactor():
    sys.stdout=open("2DscoreVsTimeFactor.txt","w")
    #testing time factor
    numRuns = 100
    masterScoreList2 = []
    timeFactorArray = [1,2,3,4,5,6,7,8,9,10]
    foxhedgeArray = ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
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
    plotScoreVsTimeFactor(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numRuns, foxhedgeArray, timeFactorArray, masterScoreList2)
    
    sys.stdout.close()  



#Functions to run
graph2D()
#graphScoreVsTimeFactor()