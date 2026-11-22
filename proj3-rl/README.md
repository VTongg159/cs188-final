# Project 3: Reinforcement Learning

Value iteration, Q-learning and approximate Q-learning on Gridworld, the crawler robot and Pacman
([assignment](https://inst.eecs.berkeley.edu/~cs188/sp26/projects/proj3/)).

- Value iteration and prioritized sweeping: [`valueIterationAgents.py`](valueIterationAgents.py)
- Q-learning and approximate Q-learning: [`qlearningAgents.py`](qlearningAgents.py)
- Parameter answers (Q2, Q3, Q7): [`analysis.py`](analysis.py)

## Autograder

```bash
cd proj3-rl
python3 autograder.py --no-graphics          # all questions: 26/25 (Q4 is extra credit)
python3 autograder.py -q q1 --no-graphics    # one question
```

## Gridworld and crawler (inside this folder)

```bash
python3 gridworld.py -a value -i 100 -k 10      # value iteration
python3 gridworld.py -a priosweepvalue -i 1000  # prioritized sweeping
python3 gridworld.py -a q -k 5 -m               # Q-learning, move with the arrow keys
python3 gridworld.py -a q -k 100 -g BridgeGrid  # Q-learning on another grid
python3 crawler.py                              # crawler robot
```

`-g` grid, `-d` discount, `-n` noise, `-r` living reward, `-e` epsilon, `-l` learning rate, `-q` no graphics.

## Pacman (from this folder or the repository root)

```bash
python3 run.py -l smallGrid     -p PacmanQAgent -x 2000 -n 2010
python3 run.py -l mediumClassic -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60
```

`-x` = number of training games (played without graphics), `-n` = total number of games.
