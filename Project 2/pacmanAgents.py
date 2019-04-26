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
import math


class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0, len(actions) - 1)]


class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0, 10):
            self.actionList.append(Directions.STOP)
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions()
        for i in range(0, len(self.actionList)):
            self.actionList[i] = possible[random.randint(0, len(possible) - 1)]
        tempState = state;
        for i in range(0, len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i])
            else:
                break
        # returns random action from all the valide actions
        return self.actionList[0]


class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = []
        for i in range(0,5):
            self.actionList.append(Directions.STOP)
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        startState = state
        bestScore = 0
        flag = False

        if startState.isWin():
            return Directions.STOP

        possible = state.getAllPossibleActions()

        for i in range(0, len(self.actionList)):
            # Generate an action sequence
            self.actionList[i] = possible[random.randint(0, len(possible) - 1)]
        tempState = state;

        for i in range(0, len((self.actionList))):
            # If current state is final state, get all successors for that state
            if tempState.isWin() + tempState.isLose() == 0:
                prevState = tempState
                tempState = tempState.generatePacmanSuccessor(self.actionList[i])
                if tempState is None:
                    flag = True
                    tempState = prevState
                    break
            else:
                break

        # Calculate best strategy for the first time
        bestScore = gameEvaluation(startState, tempState)

        # Evolving the action sequence for better score
        while flag is False:
            newScore = 0
            newSequence = self.actionList[:]
            for action in range(0, len(newSequence)):
                if random.uniform(0, 1) > 0.5:
                    newSequence[action] = possible[random.randint(0, len(possible) - 1)]
            tempState = state
            for action in range(0, len(newSequence)):
                if tempState.isWin() + tempState.isLose() == 0:
                    prevState = tempState
                    tempState = tempState.generatePacmanSuccessor(self.actionList[action])
                    if tempState is None:
                        flag = True
                        tempState = prevState
                        break
                else:
                    break

            if tempState is not state:
                newScore = gameEvaluation(state, tempState)
            if newScore >= bestScore:
                bestScore = newScore
                self.actionList = newSequence[:]

        return self.actionList[0]

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        # creating and initializing a list of 5 actions
        self.actionCount = 5;
        self.actionList = [];
        for actionCount in range(0, 5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        population = [];
        possible = state.getAllPossibleActions();
        bestAction = {"firstAction": '', "score": -1000000}

        # Generate initial population
        for i in range(0, 8):
            actionList = []
            for j in range(0, self.actionCount):
                actionList.append(possible[random.randint(0, len(possible) - 1)])
            population.append(actionList[:])

        while True:
            evaluatedCandidates = []

            for i in range(0, 8):
                tempState = state
                currentActions = population[i]

                for j in range(0, self.actionCount):
                    if tempState.isWin():
                        return currentActions[0]
                    elif tempState.isLose():
                        break;
                    else:
                        nextState = tempState.generatePacmanSuccessor(currentActions[j])
                        if nextState is None:
                            return bestAction["firstAction"]
                        else:
                            tempState = nextState
                evaluatedCandidates.append({
                    "actionSequence": currentActions[:],
                    "score": gameEvaluation(state, tempState)
                })

            rankedPopulation = sorted(evaluatedCandidates, key=lambda sequence: sequence["score"])
            bestRankedSequence = rankedPopulation[len(rankedPopulation) - 1]

            if bestRankedSequence["score"] >= bestAction["score"]:
                bestAction["firstAction"] = bestRankedSequence["actionSequence"][0]
                bestAction["score"] = bestRankedSequence["score"]

            futureGeneration = []

            # Working with next generation
            for i in range(0, int(8 / 2)):
                candidate1 = rankedPopulation[self.rankSelect()]
                candidate2 = rankedPopulation[self.rankSelect()]
                # 70% of the population test for crossover
                if random.randint(1, 10) <= 7:
                    for _ in range(0, 2):
                        child = []
                        # Generate mutation by randomly taking actions from both candidates
                        for j in range(0, self.actionCount):
                            if random.randint(0, 1) == 0:
                                child.append(candidate1['actionSequence'][j])
                            else:
                                child.append(candidate2['actionSequence'][j])
                        futureGeneration.append(child[:])
                else:
                    futureGeneration.append(candidate1['actionSequence'])
                    futureGeneration.append(candidate2['actionSequence'])

            # Applying random test for each chromosome
            for i in range(0, 8):
                if random.randint(1, 10) == 1:
                    futureGeneration[i][random.randint(0, self.actionCount - 1)] = possible[random.randint(0, len(possible) - 1)]
            population = futureGeneration

    def rankSelect(self):
        # Sum of ranks is essentially sum of consecutive numbers
        highestRankPossible = 8
        sumOfRanks = highestRankPossible * (highestRankPossible + 1) / 2
        randomInteger = random.randint(1, sumOfRanks)
        selectedRank = tempRank = highestRankPossible;
        while tempRank <= sumOfRanks:
            if randomInteger <= tempRank:
                return selectedRank - 1
            else:
                selectedRank -= 1
                tempRank += selectedRank


class MCTSAgent(Agent):
    # Called once when the game starts
    def registerInitialState(self, state):
        return;

    # Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        self.noneReached = False
        self.rootState = state

        rootNode = Node(state, None, None)

        while not self.noneReached:
            expandedNode = self.treePolicy(rootNode)
            if expandedNode == None:
                break

            rollout = self.defaultPolicy(expandedNode)
            if rollout == None:
                break

            self.backPropogation(expandedNode, rollout)

        maxVisits = max([node.numVisits for node in rootNode.childNodes])

        for node in rootNode.childNodes:
            if node.numVisits == maxVisits:
                bestNodes = [node]

        return random.choice(bestNodes).action

    def treePolicy(self, node):
        while node != None and not node.state.isWin() and not node.state.isLose():
            if not node.explorationComplete:
                return self.expand(node)
            else:
                node = self.uctSearch(node)

    def defaultPolicy(self, node):
        state = node.state
        # Perform rollout till 5 steps
        for i in range(0, 5):
            if state.isWin() + state.isLose() == 0:
                legal = state.getLegalPacmanActions()
                if not legal:
                    break
                nextState = state.generatePacmanSuccessor(random.choice(legal))
                if nextState is None:
                    self.noneReached = True
                    break
                else:
                    state = nextState
            else:
                break

        return gameEvaluation(self.rootState, state)

    def uctSearch(self, node):
        bestUCT = -99999
        bestNodes = []

        for child in node.childNodes:
            result = (child.evaluation / child.numVisits) + math.sqrt(
                (2 * math.log(node.numVisits)) / child.numVisits)
            if result == bestUCT:
                bestNodes.append(child)
            elif result > bestUCT:
                bestNodes = []
                bestNodes.append(child)
                bestUCT = result

        return bestNodes[random.randint(0, len(bestNodes)-1)]

    def expand(self, node):
        nextAction = node.legalActions.pop(random.randint(0, len(node.legalActions) - 1))
        nextState = node.state.generatePacmanSuccessor(nextAction)

        if nextState is None:
            self.noneReached = True
            return None

        nextNode = Node(nextState, node, nextAction)
        node.childNodes.append(nextNode)

        if len(node.legalActions) == 0:
            node.explorationComplete = True

        return nextNode

    def backPropogation(self, node, rollout):
        while node is not None:
            node.numVisits += 1
            node.evaluation += rollout
            node = node.parent

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.legalActions = state.getLegalPacmanActions()
        self.evaluation = 0.0
        self.numVisits = 0
        self.explorationComplete = False
        self.parent = parent
        self.childNodes = []
        self.action = action
