#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 20:30:49 2021

@author: carolineskalla
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

#plotting2 imports
# from plotting2 import log
# from plotting2 import Agent
# from plotting2 import Task
# from plotting2 import Blackboard
# from plotting2 import Initialization
# from plotting2 import MoveTask
# from plotting2 import MoveAgent
# from plotting2 import Assign
#from plotting2 import AssignUnclaimed
#from plotting2 import AgentsWork
#from plotting2 import accessSkillTypes
from plotting2 import simulation
#from plotting2 import Test3D

def Test3D():
    #3D plot of the number of agents and the prortion of generalists
    numRuns = 3
    masterScoreList3DMean = []
    masterScoreList3DSD = []
    #vary proportion of generalists
    foxhedgeArray = ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    foxhedgeArraySize = len(foxhedgeArray)
    #vary number of agents
    #agentNumbers = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 500, 1000])
    #agentNumbers = [1]
    #list = range(10, 100, 10)
    #agentNumbers.append(list)
    agentNumbers = [element for element in range(10, 1000, 50)]
    #numTasks = 10*numAgents
    i = 0
    while(i < foxhedgeArraySize):
        temp = []
        temp2 = []
        masterScoreList3DMean.append(temp)
        masterScoreList3DSD.append(temp2)
        i += 1
        
    #print(numAgents)
    #print(numTasks)
    index = 0
    for ratio in foxhedgeArray:
        for agentNum in agentNumbers:
            trials = []
            for runs in range(numRuns):
                #trials = []
                timeFactor = 2
                numAgents = agentNum
                #numTasks = agentNum*10
                #numTasks = int(agentNum*1.5)
                numTasks = agentNum*10
                foxhedge = ratio
                penalty = 0.1 
                scorecoeff = 0.1
                score = simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff)
                trials.append(score)
            #stdDev = statistics.stdev(trials)  
            print(trials)
            avg = statistics.median(trials)
           # avg = statistics.mean(trials)
           # sd = statistics.stdev(trials)
            masterScoreList3DMean[index].append(avg)
           # masterScoreList3DSD[index].append(sd)
        index += 1
     
    #plotting 3D Mean
    x = []
    y = []
    z = []
    count = 0
    
    for r in masterScoreList3DMean:
        count2 = 0
        for na in r:
            x.append(foxhedgeArray[count])
            y.append(agentNumbers[count2])
            z.append(na)
            count2 += 1
        count += 1
    np.array(x)
    np.array(y)
    np.array(z)
    
    #plotting 3D Standard Dev
    xSD = []
    ySD = []
    zSD = []
    count = 0
    
    for r in masterScoreList3DSD:
        count2 = 0
        for na in r:
            xSD.append(foxhedgeArray[count])
            ySD.append(agentNumbers[count2])
            zSD.append(na)
            count2 += 1
        count += 1
            
    """

    # Creating figure for Mean
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
         
    # Creating plot
    #ax.surface_plot(x, y, z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.scatter3D(x, y, z, color = "blue")
    plt.title("Mean Score vs Number of Agents and Proportion of Generalists")
    plt.xlabel('Proportion of Generalists')
    plt.ylabel('Number of Agents')
    ax.set_zlabel('Mean Score')
    plt.figtext(.5, 0.07, "timeFactor = " + str(timeFactor) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numRuns), ha="center", fontsize=10)
    plt.show()
    # show plot
    #plt.show()
   
    # Creating figure for Standard Dev
    fig2 = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
         
    # Creating plot
    #ax.surface_plot(x, y, z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.scatter3D(xSD, ySD, zSD, color = "blue")
    plt.title("Standard Deviation of Score vs Number of Agents and Proportion of Generalists")
    plt.xlabel('Proportion of Generalists')
    plt.ylabel('Number of Agents')
    ax.set_zlabel('Mean Score')
    plt.figtext(.5, 0.07, "timeFactor = " + str(timeFactor) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numRuns), ha="center", fontsize=10)
 
    # show plot
    plt.show()
                
    """
    
    #surface plot (of mean)
    # target grid to interpolate to
    xi = np.arange(0,1.01,0.001)
    yi = np.arange(10,1000.01,0.001)
    xi,yi = np.meshgrid(xi,yi)
    
    # interpolate
    zi = griddata((x,y),z,(xi,yi),method='linear')
    print(zi)
    """
    #plot
    fig2 = plt.figure()
    axes = fig2.gca(projection ='3d')
    axes.plot_surface(xi, yi, zi)
    #plt.plot(x,y,'k.')
    plt.xlabel('Proportion of Generalist',fontsize=10)
    plt.ylabel('Number of AGents',fontsize=10)
    axes.set_zlabel('Mean Score', fontsize=10)
    plt.title("Mean Score vs Proportion of Generalists and Number of Agents")
    plt.figtext(.5, 0.0, "timeFactor = " + str(timeFactor) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numRuns), ha="center", fontsize=10)
    plt.show()
    
    #surface plot (of Std Dev)
    # target grid to interpolate to
    xiSD = np.arange(0,1.01,0.001)
    yiSD = np.arange(10,1000.01,0.001)
    xiSD,yiSD = np.meshgrid(xi,yi)
    
    # interpolate
    ziSD = griddata((xSD,ySD),zSD,(xiSD,yiSD),method='linear')
    
    #plot
    fig3 = plt.figure()
    axes = fig3.gca(projection ='3d')
    axes.plot_surface(xiSD, yiSD, ziSD)
    #plt.plot(x,y,'k.')
    plt.xlabel('Proportion of Generalist',fontsize=10)
    plt.ylabel('Number of AGents',fontsize=10)
    axes.set_zlabel('Standard Deviation of  Score', fontsize=10)
    plt.title("Mean Score vs Proportion of Generalists and Number of Agents")
    plt.figtext(.5, 0.0, "timeFactor = " + str(timeFactor) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff) + ", numRuns = " + str(numRuns), ha="center", fontsize=10)
    plt.show()

    """
####Functions to run
#main()
#testTimeFactor()
#Test3D()
