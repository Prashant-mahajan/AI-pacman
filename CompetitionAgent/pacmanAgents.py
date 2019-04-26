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
import random
import math

class CompetitionAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state, depth='2'):
        self.index = 0
        # Used to depth limit the expectimax search, default depth is 2
        self.depth = int(depth)

    def getAction(self, gameState):
        def expectimax(state, depth, agentIndex):
            if state.isWin() or state.isLose():
                return state.getScore()
            if agentIndex == 0:  # PAC-MAN node (max node)
                newAgentIndex = agentIndex + 1
                maxScore = -float("inf")
                maxAction = Directions.STOP
                # need to generate successors
                actions = state.getLegalActions(agentIndex)
                # need to generate scores for each successor:
                for action in actions:
                    successorState = state.generateSuccessor(agentIndex, action)
                    score = expectimax(successorState, depth, newAgentIndex)
                    if score > maxScore:
                        maxScore = score
                        maxAction = action
                if depth == 0:
                    return maxAction
                else:
                    return maxScore
            else:
                # need to generate successors
                actions = state.getLegalActions(agentIndex)
                # if we are looking at the final ghost, increment the depth:
                if agentIndex == state.getNumAgents() - 1:
                    depth += 1
                    newAgentIndex = 0
                else:
                    newAgentIndex = agentIndex + 1
                # need to generate scores for each successor:
                totalScore = 0
                for action in actions:
                    # if we are at depth, evaluate the state
                    if depth == self.depth:
                        totalScore += self.betterEvaluationFunction(state.generateSuccessor(agentIndex, action))
                    # otherwise, go deeper
                    else:
                        successorState = state.generateSuccessor(agentIndex, action)
                        totalScore += expectimax(successorState, depth, newAgentIndex)
                averageScore = totalScore / len(actions)
                return averageScore

        return expectimax(gameState, 0, 0)

    def terminalConditionCheck(self, gameState):
        return gameState.isWin() or gameState.isLose()

    def betterEvaluationFunction(self, state):
        # if state.isWin():
        #     return float("inf")
        # if state.isLose():
        #     return - float("inf")
        #
        # # Active ghosts are ghosts that aren't scared.
        # scaredGhosts, activeGhosts = [], []
        #
        # currentScore = state.getScore()
        # self.pos = state.getPacmanPosition()
        #
        # # Calculate distance to closest food and no of capsules left
        # availableFood = state.getFood().asList()
        # closestFood = min(map(lambda x: self.manhattanDistance(self.pos, x), availableFood))
        # capsulesLeft, foodLeft = len(state.getCapsules()), len(availableFood)
        #
        # for ghost in state.getGhostStates():
        #     if not ghost.scaredTimer:
        #         activeGhosts.append(ghost)
        #     else:
        #         scaredGhosts.append(ghost)
        #
        # distanceToClosestActiveGhost = min(self.getManhattanDistances(activeGhosts)) if activeGhosts else float('inf')
        # # Inverse the value and multiply by -2 to make sure pacman stays away from active ghost
        # distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)
        # activeGhostsScore = - 2 * (1. / distanceToClosestActiveGhost)
        #
        # # Multiply the value by -3 to make sure pacman move towards scared ghost
        # distanceToClosestScaredGhost = min(self.getManhattanDistances(scaredGhosts)) if scaredGhosts else 0
        #
        # # To make sure pacman eats all available pellets
        # foodLeftScore = -4 * foodLeft
        # # If capsule is close it is given preference
        # capsulesLeftScore = -20 * capsulesLeft
        #
        # return currentScore + foodLeftScore + capsulesLeftScore + activeGhostsScore \
        #        - 1.5 * closestFood - 2 * distanceToClosestScaredGhost

        newPos = state.getPacmanPosition()  # get the current position of the pacman
        Food = state.getFood()  # get the grid of the food

        foodList = [self.manhattanDistance(newPos, f) for f in
                    Food.asList()]  # calculate the manhattan distance between pellets and pacman

        foodScore = 0

        for f in foodList:
            foodScore += 1.0 / float(f)  # pellets which are closer get higher score then pellets which are farther away

        newGhostStates = state.getGhostStates()  # Getting the ghost states Note: Only used to get the the scared timer so that the pacman dosent run away from the ghosts when they are scared.
        newScaredTimes = [ghostState.scaredTimer for ghostState in
                          newGhostStates]  # scared times for making the pacman eat scared ghosts

        GhostPositions = state.getGhostPositions()  # getting the positions of the ghosts.
        GhostDistance = [self.manhattanDistance(newPos, g) for g in
                         GhostPositions]  # calculate the manhattan distance between ghost and pacman.
        GhostDistance.sort()  # sort the distance to the ghosts

        GhostScore = 0
        if min(GhostDistance) == 0:  # if the ghost is very near give high penalty
            GhostScore = 100000000
        else:
            for g in GhostDistance:  # add to the ghost score
                if g < 3 and g != 0:  # if the ghost if more than distance of 3 ignore the ghost (if the ghost is very near handled earlier, handled divide be zero error)
                    GhostScore = + 1.0 / g  # nearer the ghost more is the penalty

        scaredtimeSum = sum(newScaredTimes)  # take sum of scared times for both ghosts

        return state.getScore() + foodScore - 28 * GhostScore + 1.2 * scaredtimeSum

    def getManhattanDistances(self, ghosts):
        return map(lambda g: self.manhattanDistance(self.pos, g.getPosition()), ghosts)

    def manhattanDistance(self, x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

