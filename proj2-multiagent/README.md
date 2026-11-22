# Project 2 — Multi-Agent Search

Pacman plays against ghosts using a reflex agent, Minimax, Alpha-Beta pruning, and Expectimax. A state evaluation function guides the search using food, capsules, and ghost positions. The implementation follows the [UC Berkeley CS188 Spring 2026 assignment](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj2/).

Run these commands from the repository root on the `proj2` branch or on `main` after the PR is merged. The commands were verified on Python 3.12.3.

```bash
cd proj2-multiagent
python3 -B autograder.py --no-graphics
python3 -B autograder.py -q q5 --no-graphics
```

The local autograder reports **25/25** for Q1–Q5. Q6 is the course's separate AI-use and collaboration reflection on Gradescope.

## Run Pacman

From the repository root, use `-q` to run without the GUI or replace it with `-t` for a text display. `-f` fixes the random seed for a reproducible run.

```bash
python3 -B run.py -p ReflexAgent -l testClassic -q -f
python3 -B run.py -p MinimaxAgent -l minimaxClassic -a depth=3 -q -f
python3 -B run.py -p AlphaBetaAgent -l smallClassic -a depth=3 -q -f
python3 -B run.py -p ExpectimaxAgent -l minimaxClassic -a depth=3 -q -f
python3 -B run.py -p ExpectimaxAgent -l smallClassic -a depth=2,evalFn=better -k 1 -q -n 10 -f
```

The agents and evaluation function are in [`multiAgents.py`](multiAgents.py). See the [sources and AI-use note](reports/QUESTION_MAPPING.md) for attribution.
