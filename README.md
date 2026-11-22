# CS188 Final Project

Team project based on [UC Berkeley CS188 Spring 2026](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/).

| Folder | Content |
|---|---|
| `pacman_env/` | Shared official CS188 Pacman environment (game, graphics, layouts) |
| `run.py` | Runs any Pacman agent from Project 1 or 2 |
| `proj1-search/` | Project 1: DFS, BFS, UCS, A*, heuristics |
| `proj2-multiagent/` | Project 2: Reflex, Minimax, Alpha-Beta, Expectimax |
| `proj3-rl/` | Project 3: Reinforcement Learning (not added yet) |
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

Run from the repository root or from inside `proj1-search/` or `proj2-multiagent/`:

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
cd proj5-ml          && python3 autograder.py && cd ..
```

One question only: `python3 autograder.py -q q1 --no-graphics`

## Rules for the team

- Everything lives on `main`: `git pull` before you start, `git push` when you are done.
- Commit messages start with the project: `p1: ...`, `p2: ...`, `p3: ...`, `p5: ...`; shared changes use `docs: ...` or `chore: ...`.
- Do not edit `pacman_env/`. Each project only changes its own folder.

## Notes on the shared environment

`pacman_env/` is the official Spring 2026 starter (v1.004). Its layouts are byte-identical to the official zips.
Only two changes were needed to share one copy between Projects 1 and 2:

- `game.py`: action order is fixed to the Project 2 order (West, Stop, East, North, South), which the Project 2 autograder needs.
- `layout.py`: maps are also looked up in `pacman_env/layouts/`.
