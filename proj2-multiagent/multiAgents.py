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

from collections import OrderedDict, deque

# Static geometry only: no food, ghost timers, or GameStates are cached.
# Content keys keep copied boards compatible and different layouts isolated.
_LAYOUT_CACHE = OrderedDict()


def _layout_info(walls):
    if hasattr(walls, '_multiagent_geometry'):
        return walls._multiagent_geometry
    # Avoid Grid.packBits: this starter's legacy implementation uses Python 2
    # division. A tuple of immutable byte columns is an unambiguous wall key.
    key = (walls.width, walls.height, tuple(bytes(column) for column in walls.data))
    if key not in _LAYOUT_CACHE:
        neighbors = {}
        for x in range(walls.width):
            for y in range(walls.height):
                if not walls[x][y]:
                    neighbors[x, y] = tuple((nx, ny) for nx, ny in
                        ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1))
                        if 0 <= nx < walls.width and 0 <= ny < walls.height
                        and not walls[nx][ny])
        _LAYOUT_CACHE[key] = dict(neighbors=neighbors, maps=OrderedDict(), routes={})
        if len(_LAYOUT_CACHE) > 4:
            _LAYOUT_CACHE.popitem(last=False)
    _LAYOUT_CACHE.move_to_end(key)
    info = _LAYOUT_CACHE[key]
    walls._multiagent_geometry = info
    return info


def _distance_map(position, walls):
    info = _layout_info(walls)
    maps = info['maps']
    if position not in maps:
        distances = {position: 0}
        order = []
        queue = deque([position])
        while queue:
            cell = queue.popleft()
            order.append(cell)
            for neighbor in info['neighbors'][cell]:
                if neighbor not in distances:
                    distances[neighbor] = distances[cell] + 1
                    queue.append(neighbor)
        maps[position] = distances, order
        if len(maps) > 64:
            maps.popitem(last=False)
    maps.move_to_end(position)
    return maps[position]


def _maze_distance(distances, target):
    """Support scared ghosts between grid cells, without rounding through walls."""
    from math import floor, ceil
    x, y = target
    return min((distances.get((nx, ny), float('inf')) + abs(x - nx) + abs(y - ny)
                for nx in {floor(x), ceil(x)} for ny in {floor(y), ceil(y)}),
               default=float('inf'))


def _corridor_penalty(position, ghosts, capsules, walls):
    """Penalize routes whose next junction/capsule can be intercepted by a ghost.

    This is a feature of the successor state, not an extra game-tree search.
    Ghosts move before Pacman's next move, hence the one-turn safety margin.
    """
    info = _layout_info(walls)
    neighbors = info['neighbors']
    if position not in info['routes']:
        routes = []
        for neighbor in neighbors[position]:
            path = [neighbor]
            previous, cell = position, neighbor
            seen = {position}
            while len(neighbors[cell]) == 2 and cell not in seen:
                seen.add(cell)
                following = next(n for n in neighbors[cell] if n != previous)
                previous, cell = cell, following
                path.append(cell)
            routes.append((tuple(path), len(neighbors[cell]) >= 3 and cell not in seen))
        info['routes'][position] = routes
    margins = []
    for path, has_exit in info['routes'][position]:
        # A capsule can turn a dangerous corridor into a viable escape route.
        target_index = next((i for i, cell in enumerate(path) if cell in capsules), None)
        if target_index is None:
            if not has_exit:
                continue
            target_index = len(path) - 1
            steps = target_index + 1
            target = path[target_index]
        else:
            # Reaching the capsule itself is safe even if a ghost occupies it:
            # Pacman consumes it before collision checking. Check the approach.
            steps = target_index
            target = position if steps == 0 else path[target_index - 1]
        distances, _ = _distance_map(target, walls)
        threats = [_maze_distance(distances, ghost.getPosition()) - steps - 1
                   for ghost in ghosts if ghost.scaredTimer <= steps + 1]
        margins.append(min(threats, default=float('inf')))
    best_margin = max(margins, default=float('inf'))
    return 100 + 25 * min(4, -best_margin) if best_margin <= 0 else 0


def _food_distance(position, food, walls):
    """Exact nearest-food distance using bounded caches of static BFS maps."""
    if food[position[0]][position[1]]:
        return 0
    info = _layout_info(walls)
    for x, y in info['neighbors'][position]:
        if food[x][y]:
            return 1
    distances, order = _distance_map(position, walls)
    for x, y in order:
        if food[x][y]:
            return distances[x, y]
    return 0 if food.count() == 0 else walls.width * walls.height


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

        # Self-study implementation with Codex; see reports/QUESTION_MAPPING.md.
        score = successorGameState.getScore()
        if successorGameState.isWin():
            return score + 100000
        if successorGameState.isLose():
            return score - 100000
        score -= 3 * newFood.count()
        walls = successorGameState.getWalls()
        score += 10 / (1 + _food_distance(newPos, newFood, walls))
        distances, _ = _distance_map(newPos, walls)
        for ghost in newGhostStates:
            distance = _maze_distance(distances, ghost.getPosition())
            if ghost.scaredTimer > distance + 1:
                score += 30 / (distance + 1)
            elif ghost.scaredTimer <= 1:
                score -= 12 / (distance + 0.5)
                if distance <= 1:
                    score -= 500
        score -= _corridor_penalty(newPos, newGhostStates,
                                   successorGameState.getCapsules(), walls)
        if action == Directions.STOP:
            score -= 2
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

    def _search(self, state, agent, rounds):
        if state.isWin() or state.isLose() or rounds >= self.depth:
            return self.evaluationFunction(state), Directions.STOP
        actions = state.getLegalActions(agent)
        if not actions:
            return self.evaluationFunction(state), Directions.STOP
        next_agent = (agent + 1) % state.getNumAgents()
        next_round = rounds + (next_agent == 0)
        best = float('-inf') if agent == 0 else float('inf')
        chosen = actions[0]
        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, _ = self._search(child, next_agent, next_round)
            if (agent == 0 and value > best) or (agent != 0 and value < best):
                best, chosen = value, action
        return best, chosen

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        return self._search(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def _search(self, state, agent, rounds, alpha=float('-inf'), beta=float('inf')):
        if state.isWin() or state.isLose() or rounds >= self.depth:
            return self.evaluationFunction(state), Directions.STOP
        actions = state.getLegalActions(agent)
        if not actions:
            return self.evaluationFunction(state), Directions.STOP
        next_agent = (agent + 1) % state.getNumAgents()
        next_round = rounds + (next_agent == 0)
        best = float('-inf') if agent == 0 else float('inf')
        chosen = actions[0]
        for action in actions:
            # Generate lazily: pruned children must never be generated.
            child = state.generateSuccessor(agent, action)
            value, _ = self._search(child, next_agent, next_round, alpha, beta)
            if agent == 0:
                if value > best:
                    best, chosen = value, action
                if best > beta:
                    return best, chosen
                alpha = max(alpha, best)
            else:
                if value < best:
                    best, chosen = value, action
                if best < alpha:
                    return best, chosen
                beta = min(beta, best)
        return best, chosen

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self._search(gameState, 0, 0)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def _search(self, state, agent, rounds):
        if state.isWin() or state.isLose() or rounds >= self.depth:
            return self.evaluationFunction(state), Directions.STOP
        actions = state.getLegalActions(agent)
        if not actions:
            return self.evaluationFunction(state), Directions.STOP
        next_agent = (agent + 1) % state.getNumAgents()
        next_round = rounds + (next_agent == 0)
        if agent != 0:
            total = 0.0
            for action in actions:
                child = state.generateSuccessor(agent, action)
                total += self._search(child, next_agent, next_round)[0]
            return total / len(actions), Directions.STOP
        best, chosen = float('-inf'), actions[0]
        for action in actions:
            child = state.generateSuccessor(agent, action)
            value, _ = self._search(child, next_agent, next_round)
            if value > best:
                best, chosen = value, action
        return best, chosen

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return self._search(gameState, 0, 0)[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Score plus bounded food/capsule/scared-ghost attractions,
    remaining-item penalties and active-ghost repulsion. Nearest-food distances
    use a bounded static-geometry cache, preserving the previous utility exactly.
    Terminal utilities stay finite so chance-node averages remain valid.
    Independently implemented with Codex for private study; see the report.
    """
    score = currentGameState.getScore()
    if currentGameState.isWin():
        return score + 100000
    if currentGameState.isLose():
        return score - 100000
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    walls = currentGameState.getWalls()
    score -= 4 * food.count()
    score += 10 / (1 + _food_distance(position, food, walls))
    capsules = currentGameState.getCapsules()
    score -= 15 * len(capsules)
    if capsules:
        nearest = min(manhattanDistance(position, capsule) for capsule in capsules)
        score += 6 / (nearest + 1)
    for ghost in currentGameState.getGhostStates():
        distance = manhattanDistance(position, ghost.getPosition())
        if ghost.scaredTimer > distance + 1:
            score += 100 / (distance + 1)
        elif ghost.scaredTimer <= 1:
            score -= 20 / (distance + 0.5)
            if distance <= 1:
                score -= 250
    return score

# Abbreviation
better = betterEvaluationFunction
