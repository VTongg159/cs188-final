"""Extension: the techniques of Projects 1-3 on two larger scenarios.

    python3 extension/make_layouts.py     # once: writes extension/layouts/*.lay
    python3 extension/run_extension.py    # all experiments (about 5 min, 18 processes)

Scenario A (search)    mudMaze.lay, 61 x 41, mud cells cost 5: DFS, BFS, UCS, A*.
Scenario B (game)      bigArena.lay, 41 x 23, 472 food, 3 ghosts (random or directional):
                       closest-dot search, Reflex, Alpha-Beta, Expectimax, Expectimax with a
                       maze-distance evaluation (P1 + P2), tabular and approximate Q-learning.
Prints the result tables and writes extension/results.json.
"""
import contextlib
import io
import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path[:0] = [os.path.join(ROOT, d) for d in ('pacman_env', 'proj1-search', 'proj2-multiagent', 'proj3-rl')]
os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)
import layout, pacman, ghostAgents, textDisplay, util  # noqa: E402
import search, searchAgents  # noqa: E402
import multiAgents  # noqa: E402
import qlearningAgents  # noqa: E402

MUD_MAZE = os.path.join(HERE, 'layouts', 'mudMaze.lay')
ARENA = os.path.join(HERE, 'layouts', 'bigArena.lay')
MUD_COST = 5
MOVE_CAP = 2000          # a game that is still running after this many Pacman moves is stopped
N_TEST = 20              # test games per (agent, ghost type)
N_TRAIN = 100            # training games for the Q-learning agents


# =====================================================================================
# Scenario A: search on the mud maze
# =====================================================================================
def mud_cells():
    rows = open(MUD_MAZE).read().splitlines()
    H = len(rows)
    return {(x, H - 1 - y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == '~'}


def tracked(base, attr):
    """Fringe class that remembers its largest size (memory used by the search)."""
    class Tracked(base):
        peak = 0

        def push(self, *args):
            base.push(self, *args)
            Tracked.peak = max(Tracked.peak, len(getattr(self, attr)))
    return Tracked


def run_search(name, algorithm, mud, lay):
    state = pacman.GameState()
    state.initialize(lay, 0)
    goal = state.getFood().asList()[0]
    cost = (lambda p: MUD_COST if p in mud else 1)
    problem = searchAgents.PositionSearchProblem(state, costFn=cost, goal=goal, warn=False, visualize=False)
    order, successors = [], problem.getSuccessors

    def logged(s):
        order.append(s)
        return successors(s)
    problem.getSuccessors = logged
    fringes = {'Stack': tracked(util.Stack, 'list'), 'Queue': tracked(util.Queue, 'list'),
               'PriorityQueue': tracked(util.PriorityQueue, 'heap')}
    originals = {k: getattr(util, k) for k in fringes}
    for k, v in fringes.items():
        setattr(util, k, v)
    start = time.perf_counter()
    actions = algorithm(problem)
    seconds = time.perf_counter() - start
    for k, v in originals.items():
        setattr(util, k, v)
    return dict(name=name, cost=problem.getCostOfActions(actions), steps=len(actions),
                mud_steps=sum(p in mud for p in path_cells(state.getPacmanPosition(), actions)[1:]),
                expanded=problem._expanded, peak_fringe=max(f.peak for f in fringes.values()),
                ms=seconds * 1000, order=order, actions=actions, state=state)


def path_cells(start, actions):
    cells = [start]
    for a in actions:
        dx, dy = pacman.Actions.directionToVector(a)
        cells.append((int(cells[-1][0] + dx), int(cells[-1][1] + dy)))
    return cells


def euclidean(position, problem, info={}):
    return math.dist(position, problem.goal)


ALGORITHMS = [('DFS', search.dfs), ('BFS', search.bfs), ('UCS', search.ucs),
              ('A* Manhattan', lambda p: search.aStarSearch(p, searchAgents.manhattanHeuristic)),
              ('A* Euclid', lambda p: search.aStarSearch(p, euclidean))]


def scenario_a():
    lay = layout.getLayout(MUD_MAZE)
    results = {}
    for label, mud in [('mud', mud_cells()), ('no_mud', set())]:
        rows = [run_search(n, a, mud, lay) for n, a in ALGORITHMS]
        best = min(r['cost'] for r in rows)
        for r in rows:
            r['gap'] = (r['cost'] - best) / best * 100
        results[label] = rows
        print(f'\n== Scenario A, {label} ==')
        print(f'{"algorithm":13s} {"cost":>6s} {"gap%":>6s} {"steps":>6s} {"mud":>4s} {"expanded":>9s} '
              f'{"fringe":>7s} {"ms":>8s}')
        for r in rows:
            print(f'{r["name"]:13s} {r["cost"]:6d} {r["gap"]:6.1f} {r["steps"]:6d} {r["mud_steps"]:4d} '
                  f'{r["expanded"]:9d} {r["peak_fringe"]:7d} {r["ms"]:8.1f}')
    return results


def scenario_a2(n_food=6, seed=3):
    """Collect n_food dots spread over the maze (unit costs): FoodSearchProblem."""
    lay = layout.getLayout(MUD_MAZE)
    rng = random.Random(seed)
    free = [(x, y) for x in range(lay.width) for y in range(lay.height) if not lay.walls[x][y]]
    lay.food = lay.food.copy()
    for x, y in rng.sample(free, n_food - 1):
        lay.food[x][y] = True
    state = pacman.GameState()
    state.initialize(lay, 0)
    rows = []
    runs = [('UCS', lambda p: search.ucs(p)),
            ('A* foodHeuristic', lambda p: search.aStarSearch(p, searchAgents.foodHeuristic))]
    for name, algorithm in runs:
        problem = searchAgents.FoodSearchProblem(state)
        start = time.perf_counter()
        actions = algorithm(problem)
        rows.append(dict(name=name, cost=len(actions), expanded=problem._expanded,
                         ms=(time.perf_counter() - start) * 1000, actions=actions))
    agent = searchAgents.ClosestDotSearchAgent()
    start = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        agent.registerInitialState(state)
    rows.append(dict(name='ClosestDot (BFS lặp)', cost=len(agent.actions), expanded=None,
                     ms=(time.perf_counter() - start) * 1000, actions=agent.actions))
    best = min(r['cost'] for r in rows)
    print(f'\n== Scenario A2: collect {n_food} dots on the maze ==')
    for r in rows:
        r['gap'] = (r['cost'] - best) / best * 100
        print(f'{r["name"]:22s} cost {r["cost"]:5d} gap {r["gap"]:5.1f}% expanded {r["expanded"]} '
              f'{r["ms"]:9.1f} ms')
    return rows, state


# =====================================================================================
# Scenario B: full games on the big arena
# =====================================================================================
class Meter(textDisplay.NullGraphics):
    """No graphics; counts Pacman moves and stops the game after MOVE_CAP moves."""
    def initialize(self, state, isBlue=False):
        self.moves, self.capped = 0, False

    def update(self, state):
        if state._agentMoved == 0:
            self.moves += 1
            if self.moves >= MOVE_CAP and not (state._win or state._lose):
                self.capped = True
                self.game.gameOver = True


def ghost_team(kind, n=3):
    cls = ghostAgents.RandomGhost if kind == 'random' else ghostAgents.DirectionalGhost
    return [cls(i + 1) for i in range(n)]


def timed(agent):
    """Adds the wall-clock time spent in registerInitialState and getAction to agent.compute."""
    agent.compute = 0.0
    for method in ('registerInitialState', 'getAction'):
        if hasattr(agent, method):
            original = getattr(agent, method)

            def wrapper(state, original=original):
                start = time.perf_counter()
                result = original(state)
                agent.compute += time.perf_counter() - start
                return result
            setattr(agent, method, wrapper)
    return agent


def play(agent, kind, seed, display=None):
    """One game; returns the metrics of the report."""
    random.seed(seed)
    lay = layout.getLayout(ARENA)
    display = display or Meter()
    rules = pacman.ClassicGameRules(timeout=30)
    game = rules.newGame(lay, agent, ghost_team(kind), display, quiet=True, catchExceptions=False)
    display.game = game
    agent.compute = 0.0
    game.run()
    s = game.state
    food_total = lay.food.count()
    food_eaten = food_total - s.getNumFood()
    moves = display.moves if hasattr(display, 'moves') else 0
    score = s.getScore()
    ghosts = round((score - 10 * food_eaten - 500 * s.isWin() + 500 * s.isLose() + moves) / 200)
    return dict(win=s.isWin(), lose=s.isLose(), capped=getattr(display, 'capped', False), score=score,
                food=food_eaten / food_total, moves=moves, ghosts=ghosts,
                ms_per_move=agent.compute / max(moves, 1) * 1000)


_DIST = {}


def maze_distances(walls):
    """All-pairs maze distances (one BFS per open cell), computed once per layout."""
    key = str(walls)
    if key not in _DIST:
        cells = [(x, y) for x in range(walls.width) for y in range(walls.height) if not walls[x][y]]
        table = {}
        for source in cells:
            dist, frontier = {source: 0}, [source]
            for x, y in frontier:
                for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if not walls[n[0]][n[1]] and n not in dist:
                        dist[n] = dist[(x, y)] + 1
                        frontier.append(n)
            table[source] = dist
        _DIST[key] = table
    return _DIST[key]


def maze_evaluation(state):
    """betterEvaluationFunction of Project 2 with Manhattan distance replaced by the true
    maze distance (BFS of Project 1), and a wider danger zone around active ghosts."""
    if state.isWin() or state.isLose():
        return state.getScore()
    d = maze_distances(state.getWalls())[state.getPacmanPosition()]
    food = state.getFood().asList()
    score = state.getScore() + 10 / min(d[f] for f in food) - 4 * len(food) - 20 * len(state.getCapsules())
    for ghost in state.getGhostStates():
        distance = d.get(util.nearestPoint(ghost.getPosition()), 99)
        if ghost.scaredTimer > distance:
            score += 200 / (distance + 1)
        elif distance <= 1:
            score -= 500
        elif distance == 2:
            score -= 100
    return score


def make_agent(name):
    if name == 'ClosestDot':
        return searchAgents.ClosestDotSearchAgent()
    if name == 'Reflex':
        return multiAgents.ReflexAgent()
    if name == 'AlphaBeta':
        return multiAgents.AlphaBetaAgent(evalFn='better', depth='2')
    if name == 'Expectimax':
        return multiAgents.ExpectimaxAgent(evalFn='better', depth='2')
    if name == 'ExpectimaxMaze':
        agent = multiAgents.ExpectimaxAgent(depth='2')
        agent.evaluationFunction = maze_evaluation
        return agent
    raise ValueError(name)


def test_game(job):
    name, kind, seed = job
    with contextlib.redirect_stdout(io.StringIO()):
        return name, kind, play(timed(make_agent(name)), kind, seed)


def learn_and_test(job):
    """Trains a Q-learning agent for N_TRAIN games, then plays N_TEST test games."""
    with contextlib.redirect_stdout(io.StringIO()):
        return _learn_and_test(job)


def _learn_and_test(job):
    name, kind = job
    if name == 'ApproxQ':
        agent = qlearningAgents.ApproximateQAgent(extractor='SimpleExtractor', numTraining=N_TRAIN)
    else:
        agent = qlearningAgents.PacmanQAgent(numTraining=N_TRAIN)
    timed(agent)
    curve = []
    for i in range(N_TRAIN):
        m = play(agent, kind, 10_000 + i)
        curve.append(dict(win=m['win'], score=m['score'], food=m['food']))
    tests = [play(agent, kind, 1000 + i) for i in range(N_TEST)]
    weights = dict(agent.getWeights()) if name == 'ApproxQ' else None
    return name, kind, tests, curve, weights


AGENTS = ['ClosestDot', 'Reflex', 'AlphaBeta', 'Expectimax', 'ExpectimaxMaze', 'TabularQ', 'ApproxQ']
KINDS = ['random', 'directional']


def scenario_b():
    jobs = [(n, k, 1000 + i) for n in AGENTS[:5] for k in KINDS for i in range(N_TEST)]
    learn_jobs = [(n, k) for n in AGENTS[5:] for k in KINDS]
    games, curves, weights = {}, {}, {}
    with Pool(18) as pool:
        learning = pool.map_async(learn_and_test, learn_jobs)
        for name, kind, m in pool.imap_unordered(test_game, jobs):
            games.setdefault(f'{name}|{kind}', []).append(m)
        for name, kind, tests, curve, w in learning.get():
            games[f'{name}|{kind}'] = tests
            curves[f'{name}|{kind}'] = curve
            weights[f'{name}|{kind}'] = w
    return games, curves, weights


def summarize(games):
    import statistics as st
    table = {}
    for key, ms in games.items():
        n = len(ms)
        wins = sum(m['win'] for m in ms)
        p = wins / n                                   # 95% Wilson interval for the win rate
        z = 1.96
        centre = (p + z * z / (2 * n)) / (1 + z * z / n)
        half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        table[key] = dict(n=n, wins=wins, win_low=max(0, centre - half), win_high=min(1, centre + half),
                          capped=sum(m['capped'] for m in ms),
                          score=st.mean(m['score'] for m in ms), score_sd=st.pstdev(m['score'] for m in ms),
                          food=st.mean(m['food'] for m in ms), moves=st.mean(m['moves'] for m in ms),
                          ghosts=st.mean(m['ghosts'] for m in ms),
                          ms_per_move=st.mean(m['ms_per_move'] for m in ms))
    return table


if __name__ == '__main__':
    a = scenario_a()
    a2, _ = scenario_a2()
    t0 = time.time()
    games, curves, weights = scenario_b()
    table = summarize(games)
    print(f'\n== Scenario B ({time.time() - t0:.0f} s) ==')
    print(f'{"agent":11s} {"ghosts":12s} {"win":>6s} {"95% CI":>12s} {"cap":>4s} {"score":>8s} {"sd":>6s} '
          f'{"food%":>6s} {"moves":>6s} {"eaten":>6s} {"ms/move":>8s}')
    for n in AGENTS:
        for k in KINDS:
            r = table[f'{n}|{k}']
            print(f'{n:11s} {k:12s} {r["wins"]:3d}/{r["n"]:2d} [{r["win_low"]:.2f}, {r["win_high"]:.2f}] '
                  f'{r["capped"]:4d} {r["score"]:8.1f} {r["score_sd"]:6.1f} {r["food"] * 100:6.1f} '
                  f'{r["moves"]:6.0f} {r["ghosts"]:6.2f} {r["ms_per_move"]:8.2f}')
    for key, w in weights.items():
        if w:
            print(key, {f: round(v, 1) for f, v in w.items()})
    strip = lambda rows: [{k: v for k, v in r.items() if k not in ('order', 'actions', 'state')} for r in rows]
    json.dump(dict(scenario_a={k: strip(v) for k, v in a.items()}, scenario_a2=strip(a2), scenario_b=table, games=games,
                   curves=curves, weights=weights),
              open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
