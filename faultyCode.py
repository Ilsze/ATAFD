


#Plots Agents/Tasks vs Time and Number completed tasks vs time (for 1 simulation run)
    #Initially gave us many lines on one graph but now it doesn't.
    plt.figure(1)
    plt.plot(time, idleAgentsSize, label = "idleAgents")
    plt.plot(time, busyAgentsSize, label = "busyAgents")
    #plt.plot(time, unclaimedTasks, label = "unclaimedTasks")
    #plt.plot(time, claimedTasks, label = "claimedTasks")
    plt.title('Number of Agents vs. Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Agents')
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.32, 1.025), fancybox=True)
    #plt.legend()
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff), ha="center", fontsize=9) 
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    
    
    plt.figure(2)
    plt.plot(time, completedTasks, label = "completedTasks")
    plt.title('Number of Completed Tasks vs. Time')
    plt.xlabel('Time')
    plt.ylabel('Number of completed tasks')
    plt.figtext(.5, 0, "timeFactor = " + str(timeFactor) + ", numAgents = " + str(numAgents) + ", numTasks = " + str(numTasks) + ", penalty = " + str(penalty) +  ", scorecoeff = " + str(scorecoeff), ha="center", fontsize=9) 
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    

#Not sure what this is but it's probably useless
    #fill in sublists of masterScoreList. Each contains scores from one foxhedge ratio
        numRuns = 5
        numTrials = numRuns
        while(numRuns > 0):
            index = 0
            for tf in timefactorArray:
                #timeFactor = 2, 10 agents, 15 tasks, ratio
                timeFactor = tf
                numAgents = 10
                numTasks = 15
                foxhedge = ratio
                penalty = 0.1 
                scorecoeff = 0.1
                score = simulation(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff)
                masterScoreList[index].append(score)
                index += 1
            numRuns -= 1
            
        plotScores(timeFactor, numAgents, numTasks, foxhedge, penalty, scorecoeff, numTrials, foxhedgeArray, masterScoreList) 


#Competition supporting code
    MakeCompetitors(blackboard.idleAgents, blackboard.competingAgents)    
    #randomize order of task lists
    random.shuffle(blackboard.unclaimedTasks)
    random.shuffle(blackboard.claimedTasks)
    #main competing function
    Reassign(blackboard.competingAgents, blackboard.claimedTasks, blackboard.busyAgents, blackboard.idleAgents, timeFactor)
    #move agents in competing list back to idle list
    RemoveCompetitors(blackboard.competingAgents, blackboard.idleAgents)
    #agents work again
    #remember to increment timer appropriately


#Competition code

"""
Parameters (Type Name):
    List[Agents] idleAgents
    List[Agent] competingAgents
"""    
def MakeCompetitors(idleAgents, competingAgents):
    if idleAgents is not None:
        for agent in list(idleAgents):

            MoveAgent(agent, idleAgents, competingAgents)
 

"""
Parameters (Type Name):
    List[Agent] competingAgents
    List[Agents] idleAgents
"""    
def RemoveCompetitors(competingAgents, idleAgents):
    if idleAgents is not None:
        for agent in list(competingAgents):
            
            MoveAgent(agent, competingAgents, idleAgents)

    
"""
Parameters (Type Name):
    List[Agents] competingAgents
    List[Tasks]  claimedTasks
    List[Agents] busyAgents
    List[Agents] idleAgents
    Integer      timeFactor
"""    
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


#Attempts at importing
    #attempt 1 (failure)
    import importlib
    moduleName = input('plotting2')
    importlib.import_module(plotting2)

    #attempt 2 (failure)
    import os 
    os.system("python plotting2,py")
