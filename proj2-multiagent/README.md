# Project 2: Multi-Agent Search

Pacman plays against ghosts with a reflex agent, Minimax, Alpha-Beta and Expectimax ([assignment](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj2/)).

- Agents and evaluation functions: [`multiAgents.py`](multiAgents.py)

## Autograder

```bash
cd proj2-multiagent
python3 autograder.py --no-graphics          # all questions: 25/25
python3 autograder.py -q q2 --no-graphics    # one question
```

## Run Pacman (from this folder or the repository root)

```bash
python3 run.py -l testClassic    -p ReflexAgent
python3 run.py -l minimaxClassic -p MinimaxAgent    -a depth=3
python3 run.py -l smallClassic   -p AlphaBetaAgent  -a depth=3
python3 run.py -l minimaxClassic -p ExpectimaxAgent -a depth=3
python3 run.py -l smallClassic   -p ExpectimaxAgent -a evalFn=better -n 10 -q
```

Add `-q` to skip the graphics, `-f` to play the same game every run.
MinimaxAgent often loses on `minimaxClassic`: it assumes the ghosts play perfectly. Expectimax wins there.
