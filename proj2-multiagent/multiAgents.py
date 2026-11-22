# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = successorGameState.getScore()

        # Move towards the closest food.
        foodList = newFood.asList()
        if foodList:
            closestFood = min(manhattanDistance(newPos, food) for food in foodList)
            score += 10 / closestFood

        # Chase scared ghosts, run away from active ghosts that are close.
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            distance = manhattanDistance(newPos, ghostState.getPosition())
            if scaredTime > distance:
                score += 200 / (distance + 1)
            elif distance <= 1:
                score -= 500

        # Standing still wastes time.
        if action == Directions.STOP:
            score -= 10
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        bestValue, bestAction = float('-inf'), None
        for action in gameState.getLegalActions(0):
            value = self.minValue(gameState.generateSuccessor(0, action), 1, 0)
            if value > bestValue:
                bestValue, bestAction = value, action
        return bestAction

    def maxValue(self, state, depth):
        """Pacman (agent 0) picks the move with the highest value."""
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        value = float('-inf')
        for action in state.getLegalActions(0):
            value = max(value, self.minValue(state.generateSuccessor(0, action), 1, depth))
        return value

    def minValue(self, state, agentIndex, depth):
        """Ghost agentIndex picks the move with the lowest value."""
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        value = float('inf')
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == state.getNumAgents() - 1:
                # Last ghost moved: one ply is done, back to Pacman.
                value = min(value, self.maxValue(successor, depth + 1))
            else:
                value = min(value, self.minValue(successor, agentIndex + 1, depth))
        return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha, beta = float('-inf'), float('inf')
        bestValue, bestAction = float('-inf'), None
        for action in gameState.getLegalActions(0):
            value = self.minValue(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if value > bestValue:
                bestValue, bestAction = value, action
            alpha = max(alpha, bestValue)
        return bestAction

    def maxValue(self, state, depth, alpha, beta):
        """alpha = best value Pacman can already guarantee on this path."""
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        value = float('-inf')
        for action in state.getLegalActions(0):
            value = max(value, self.minValue(state.generateSuccessor(0, action), 1, depth, alpha, beta))
            if value > beta:          # the ghost above will never allow this
                return value
            alpha = max(alpha, value)
        return value

    def minValue(self, state, agentIndex, depth, alpha, beta):
        """beta = best (lowest) value the ghosts can already guarantee."""
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        value = float('inf')
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == state.getNumAgents() - 1:
                value = min(value, self.maxValue(successor, depth + 1, alpha, beta))
            else:
                value = min(value, self.minValue(successor, agentIndex + 1, depth, alpha, beta))
            if value < alpha:         # Pacman above will never allow this
                return value
            beta = min(beta, value)
        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        bestValue, bestAction = float('-inf'), None
        for action in gameState.getLegalActions(0):
            value = self.expValue(gameState.generateSuccessor(0, action), 1, 0)
            if value > bestValue:
                bestValue, bestAction = value, action
        return bestAction

    def maxValue(self, state, depth):
        """Pacman (agent 0) picks the move with the highest value."""
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        value = float('-inf')
        for action in state.getLegalActions(0):
            value = max(value, self.expValue(state.generateSuccessor(0, action), 1, depth))
        return value

    def expValue(self, state, agentIndex, depth):
        """Ghost agentIndex moves uniformly at random: average of the children."""
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        actions = state.getLegalActions(agentIndex)
        total = 0
        for action in actions:
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == state.getNumAgents() - 1:
                total += self.maxValue(successor, depth + 1)
            else:
                total += self.expValue(successor, agentIndex + 1, depth)
        return total / len(actions)


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: start from the game score, then
      - reward being close to the nearest food (10 / distance),
      - penalize every food and capsule left on the board,
      - chase scared ghosts that can be reached in time,
      - stay away from active ghosts (big penalty when adjacent).
    """
    if currentGameState.isWin() or currentGameState.isLose():
        return currentGameState.getScore()

    position = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    closestFood = min(manhattanDistance(position, food) for food in foodList)
    score += 10 / closestFood
    score -= 4 * len(foodList)
    score -= 20 * len(capsules)

    for ghostState in currentGameState.getGhostStates():
        distance = manhattanDistance(position, ghostState.getPosition())
        if ghostState.scaredTimer > distance:
            score += 200 / (distance + 1)
        elif distance <= 1:
            score -= 500
    return score

# Abbreviation
better = betterEvaluationFunction
