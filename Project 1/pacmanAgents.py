# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        successorsAll = []
        visited = []

        nodeInfo = dict()
        nodeInfo[state] = (None, 0)

        bestNode = None
        minCost = 100000000

        successorsAll.append(state)

        while successorsAll:
            currentNode = successorsAll.pop(0)

            if currentNode is None:
                continue

            visited.append(currentNode)
            legal = currentNode.getLegalPacmanActions()

            # Get all possible successors of the current node
            successor = [(currentNode.generatePacmanSuccessor(action), action) for action in legal]

            for eachSuccessor in successor:
                currentState, direction = eachSuccessor[0], eachSuccessor[1]

                if currentState not in visited:
                    if currentState is None:
                        tempCost = nodeInfo[currentNode][1]
                        if tempCost <= minCost:
                            minCost = tempCost
                            bestNode = currentNode

                    elif currentState.isLose() is False or currentState.isWin() is True or currentState.isWin() is False:
                        successorsAll.append(currentState)
                        cost = 1 + nodeInfo[currentNode][1] + admissibleHeuristic(currentNode)
                        if nodeInfo[currentNode][0] is None:
                            tempDirection = direction
                        else:
                            tempDirection = nodeInfo[currentNode][0]
                        nodeInfo[currentState] = (tempDirection, cost)
                else:
                    continue

        bestAction = nodeInfo[bestNode][0]
        return bestAction


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        successorsAll = []
        visited = []

        nodeInfo = dict()
        nodeInfo[state] = (None, 0)

        bestNode = None
        minCost = 100000000

        successorsAll.append(state)

        while successorsAll:
            currentNode = successorsAll.pop()

            if currentNode is None:
                continue

            visited.append(currentNode)
            legal = currentNode.getLegalPacmanActions()

            # Get all possible successors of the current node
            successor = [(currentNode.generatePacmanSuccessor(action), action) for action in legal]

            for eachSuccessor in successor:
                currentState, direction = eachSuccessor[0], eachSuccessor[1]

                if currentState not in visited:
                    if currentState is None:
                        tempCost = nodeInfo[currentNode][1]
                        if tempCost <= minCost:
                            minCost = tempCost
                            bestNode = currentNode

                    elif currentState.isLose() is False or currentState.isWin() is True or currentState.isWin() is False:
                        successorsAll.append(currentState)
                        cost = 1 + nodeInfo[currentNode][1] + admissibleHeuristic(currentNode)
                        if nodeInfo[currentNode][0] is None:
                            tempDirection = direction
                        else:
                            tempDirection = nodeInfo[currentNode][0]
                        nodeInfo[currentState] = (tempDirection, cost)
                else:
                    continue

        bestAction = nodeInfo[bestNode][0]
        return bestAction

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        successorsAll = []
        visited = []

        nodeInfo = dict()
        nodeInfo[state] = (None, 0)

        bestNode = None
        minCost = 100000000

        successorsAll.append((state, 0))

        while successorsAll:
            successorsAll.sort(key=lambda successorsAll:successorsAll[1])
            currentNode = successorsAll.pop(0)[0]

            if currentNode is None:
                continue

            visited.append(currentNode)
            legal = currentNode.getLegalPacmanActions()

            # Get all possible successors of the current node
            successor = [(currentNode.generatePacmanSuccessor(action), action) for action in legal]

            for eachSuccessor in successor:
                currentState, direction = eachSuccessor[0], eachSuccessor[1]

                if currentState not in visited:
                    if currentState is None:
                        tempCost = nodeInfo[currentNode][1]
                        if tempCost <= minCost:
                            minCost = tempCost
                            bestNode = currentNode

                    elif currentState.isLose() is False or currentState.isWin() is True or currentState.isWin() is False:

                        cost = 1 + nodeInfo[currentNode][1] + admissibleHeuristic(currentNode)
                        successorsAll.append((currentState, cost))
                        if nodeInfo[currentNode][0] is None:
                            tempDirection = direction
                        else:
                            tempDirection = nodeInfo[currentNode][0]
                        nodeInfo[currentState] = (tempDirection, cost)
                else:
                    continue

        bestAction = nodeInfo[bestNode][0]
        return bestAction
