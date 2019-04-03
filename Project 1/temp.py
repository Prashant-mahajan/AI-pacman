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

        # Store in the form of [(state, action, cost)]
        # successorsAll.append([(state, "Stop", 0)])
        #
        # while successorsAll:
        #     currentNode = successorsAll.pop()
        #     currentState = currentNode[-1][0]
        #
        #     if currentState is None:
        #         continue
        #
        #     if currentState.isWin() is True:
        #         print(successorsAll[1:])
        #         for eachSuccessor in successorsAll[1:]:
        #             for action in eachSuccessor:
        #                 a.append(action[1])
        #         # a = [action[1] for action in successorsAll]
        #         # print(a)
        #         return [action[1] for action in successorsAll][1:]
        #
        #     if currentState not in visited:
        #         visited.append(currentState)
        #
        #         # Get all possible legal actions for current node
        #         legal = currentState.getLegalPacmanActions()
        #
        #         # Get all possible successors of the current node
        #         successor = [(currentState.generatePacmanSuccessor(action), action) for action in legal]
        #
        #         # evaluate the successor states using scoreEvaluation heuristic
        #         scored = [(admissibleHeuristic(state), action) for state, action in successor]
        #
        #         state = [(i,j,k) for (i, j), (k,l) in zip(successor, scored)]
        #
        #         for node in state:
        #             if node[0] not in visited:
        #
        #                 nodePath = currentNode[:]
        #                 nodePath.append(node)
        #                 successorsAll.append(nodePath)
        #
        # return False

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
            currentNode = successorsAll.pop(-1)

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
        q = []  # queue to store the elements
        visited = []  # visited to keep track of explored nodes
        p_info = dict()  # to keep the actions to go from root node to a particular node
        total_cost_info = dict()  # to keep the total cost of the node

        q.append((state, 0))  # putting the statring node in queue
        p_info[state] = []
        total_cost_info[state] = 0
        best_node = None
        best_node_cost = 100000

        while q:

            q.sort(key=lambda q: q[1])  # sorting the queue
            s = q.pop(0)[0]  # pop the first node from queue
            if s == None:
                continue

            if s not in visited:
                visited.append(s)
                legal = s.getLegalPacmanActions()
                successors = [(s.generatePacmanSuccessor(action), action) for action in
                              legal]  # generate all successor of the node
                for suc in successors:
                    if suc[0] is None:  # if successor id none then node is leaf node, calculating the best leaf node.
                        if total_cost_info[s] < best_node_cost:
                            best_node = s
                            best_node_cost = total_cost_info[s]
                    else:
                        total_cost_info[suc[0]] = 1 + total_cost_info[s] + admissibleHeuristic(
                            s)  # total cost of the node.
                        t = total_cost_info[suc[0]]
                        q.append((suc[0], t))  # put the successor and total cost in queue
                        p_info[suc[0]] = []  # put information of actions to reach the successor
                        p_info[suc[0]].extend(p_info[s])
                        p_info[suc[0]].append(suc[1])

        l = p_info[best_node]
        act = l[0]  # return single action that leads to best node

        return act

