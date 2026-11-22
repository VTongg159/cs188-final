# CS188 Final Project

Team project based on [UC Berkeley CS188 Spring 2026](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/).

| Folder | Content |
|---|---|
| `pacman_env/` | Shared official CS188 Pacman environment (game, graphics, layouts) |
| `run.py` | Runs any Pacman agent from Projects 1, 2 and 3 |
| `proj1-search/` | Project 1: DFS, BFS, UCS, A*, heuristics |
| `proj2-multiagent/` | Project 2: Reflex, Minimax, Alpha-Beta, Expectimax |
| `proj3-rl/` | Project 3: Value Iteration, Q-Learning, Approximate Q-Learning |
| `proj5-ml/` | Project 5: Machine Learning (PyTorch) |

## Setup

```bash
git clone https://github.com/VTongg159/cs188-final.git
cd cs188-final
pip install "numpy<2.0" matplotlib                                   # Project 5 also needs:
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Python 3.10 or newer.

## Run Pacman

Run from the repository root or from inside any project folder (`proj1-search/`, `proj2-multiagent/`, `proj3-rl/`):

```bash
python3 run.py -l <map> -p <agent> [-a <agent args>]
```

Project 1 (Search):

```bash
python3 run.py -l mediumMaze    -p SearchAgent -a fn=dfs
python3 run.py -l mediumMaze    -p SearchAgent -a fn=bfs
python3 run.py -l mediumMaze    -p SearchAgent -a fn=ucs
python3 run.py -l bigMaze       -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python3 run.py -l mediumCorners -p AStarCornersAgent
python3 run.py -l trickySearch  -p AStarFoodSearchAgent
python3 run.py -l bigSearch     -p ClosestDotSearchAgent
```

Project 2 (Multi-agent):

```bash
python3 run.py -l testClassic    -p ReflexAgent
python3 run.py -l minimaxClassic -p MinimaxAgent    -a depth=3
python3 run.py -l smallClassic   -p AlphaBetaAgent  -a depth=3
python3 run.py -l minimaxClassic -p ExpectimaxAgent -a depth=3
python3 run.py -l smallClassic   -p ExpectimaxAgent -a evalFn=better
```

Project 3 (Reinforcement learning), `-x` = training games (no graphics), `-n` = total games:

```bash
python3 run.py -l smallGrid     -p PacmanQAgent    -x 2000 -n 2010
python3 run.py -l mediumClassic -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60
```

Gridworld and crawler (Project 3, run inside `proj3-rl/`):

```bash
cd proj3-rl
python3 gridworld.py -a value -i 100 -k 10     # value iteration, 100 iterations, 10 episodes
python3 gridworld.py -a priosweepvalue -i 1000 # prioritized sweeping
python3 gridworld.py -a q -k 5 -m              # Q-learning, you move with the arrow keys
python3 gridworld.py -a q -k 100 -g BridgeGrid # Q-learning on another grid
python3 crawler.py                             # Q-learning crawler robot
```

Gridworld options: `-g` grid (BookGrid, BridgeGrid, CliffGrid, DiscountGrid, MazeGrid), `-d` discount, `-n` noise, `-r` living reward, `-e` epsilon, `-l` learning rate, `-q` no graphics.

Useful options:

| Option | Meaning |
|---|---|
| `-q` | no graphics, print the result only |
| `-t` | text graphics in the terminal |
| `-n 10` | play 10 games |
| `-k 1` | number of ghosts |
| `-f` | fixed random seed (same game every run) |
| `--frameTime 0` | fastest animation |

Maps are in `pacman_env/layouts/` (official CS188 maps). All options: `python3 run.py --help`.

## Autograder

```bash
cd proj1-search      && python3 autograder.py --no-graphics && cd ..   # 26/25
cd proj2-multiagent  && python3 autograder.py --no-graphics && cd ..   # 25/25
cd proj3-rl          && python3 autograder.py --no-graphics && cd ..   # 26/25
cd proj5-ml          && python3 autograder.py && cd ..
```

One question only: `python3 autograder.py -q q1 --no-graphics`

## Rules for the team

- Everything lives on `main`: `git pull` before you start, `git push` when you are done.
- Commit messages start with the project: `p1: ...`, `p2: ...`, `p3: ...`, `p5: ...`; shared changes use `docs: ...` or `chore: ...`.
- Do not edit `pacman_env/`. Each project only changes its own folder.

## Notes on the shared environment

`pacman_env/` is the official Spring 2026 starter (v1.004). Its layouts are byte-identical to the official zips
(`smallGrid` and `mediumGrid` come from the Project 3 zip). The Project 2 and Project 3 starters ship the same framework.
Changes needed to share one copy (only the first two touch `pacman_env/`):

- `game.py`: action order is fixed to the Project 2 order (West, Stop, East, North, South), which the Project 2 autograder needs.
- `layout.py`: maps are also looked up in `pacman_env/layouts/`.
- Project 3: the recorded test data (`Experiences`) moved unchanged from its `util.py` to `proj3-rl/experiences.py`.
- Entry scripts (`autograder.py`, `gridworld.py`, `crawler.py`) add `../pacman_env` to the Python path.
