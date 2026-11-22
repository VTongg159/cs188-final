# Project 1 — Search

Pacman uses DFS, BFS, uniform-cost search, and A* to navigate mazes and collect food. The implementation follows the [UC Berkeley CS188 Spring 2026 assignment](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj1/).

Run these commands from the repository root on the `proj1` branch or on `main` after the PR is merged. The commands were verified on Python 3.12.3.

```bash
cd proj1-search
python3 -B autograder.py --no-graphics
python3 -B autograder.py -q q6 --no-graphics
```

The local autograder reports **26/25**, including the bonus point for Q7. Q9 is the course's separate AI-use and collaboration reflection on Gradescope.

## Run Pacman

From `proj1-search/`, use `-q` to run without the GUI or replace it with `-t` for a text display.

```bash
python3 -B pacman.py -l mediumMaze -p SearchAgent -a fn=dfs -q
python3 -B pacman.py -l mediumMaze -p SearchAgent -a fn=bfs -q
python3 -B pacman.py -l mediumMaze -p SearchAgent -a fn=ucs -q
python3 -B pacman.py -l bigMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic -q
python3 -B pacman.py -l mediumCorners -p AStarCornersAgent -q
python3 -B pacman.py -l trickySearch -p AStarFoodSearchAgent -q
python3 -B pacman.py -l bigSearch -p ClosestDotSearchAgent -q
```

The search algorithms are in [`search.py`](search.py). Pacman agents, search problems, and heuristics are in [`searchAgents.py`](searchAgents.py). See the [sources and AI-use note](reports/QUESTION_MAPPING.md) for attribution.
