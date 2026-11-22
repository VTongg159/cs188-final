# Project 1: Search

Pacman finds paths with DFS, BFS, UCS and A* ([assignment](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj1/)).

- Algorithms: [`search.py`](search.py)
- Search problems and heuristics: [`searchAgents.py`](searchAgents.py)
- Sources and AI-use note: [`reports/QUESTION_MAPPING.md`](reports/QUESTION_MAPPING.md)

## Autograder

```bash
cd proj1-search
python3 autograder.py --no-graphics          # all questions: 26/25
python3 autograder.py -q q1 --no-graphics    # one question
```

## Run Pacman (from this folder or the repository root)

```bash
python3 run.py -l mediumMaze    -p SearchAgent -a fn=dfs
python3 run.py -l mediumMaze    -p SearchAgent -a fn=bfs
python3 run.py -l mediumMaze    -p SearchAgent -a fn=ucs
python3 run.py -l bigMaze       -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python3 run.py -l mediumCorners -p AStarCornersAgent
python3 run.py -l trickySearch  -p AStarFoodSearchAgent
python3 run.py -l bigSearch     -p ClosestDotSearchAgent
```

Add `-q` to skip the graphics.
