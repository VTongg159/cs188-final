"""Run any Pacman agent from Projects 1, 2 or 3 in the shared environment.

Usage (from the repository root):
    python run.py -l mediumMaze -p SearchAgent -a fn=bfs
    python run.py -l smallClassic -p AlphaBetaAgent -a depth=3
    python run.py --help          # all pacman.py options

Add -q for no graphics, -t for text graphics, -f for a fixed random seed.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIRS = [os.path.join(ROOT, name)
        for name in ('pacman_env', 'proj1-search', 'proj2-multiagent', 'proj3-rl')]

# pacman.py finds agents (files ending in "gents.py") through $PYTHONPATH.
sys.path[:0] = DIRS
os.environ['PYTHONPATH'] = os.pathsep.join(DIRS + [os.environ.get('PYTHONPATH', '')])

import pacman  # noqa: E402  (must come after the path setup)

if __name__ == '__main__':
    pacman.runGames(**pacman.readCommand(sys.argv[1:]))
