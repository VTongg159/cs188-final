"""Shortcut so that `python3 run.py ...` also works inside this folder.
It simply runs ../run.py (the shared Pacman environment) with the same options."""
import os
import runpy

runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'run.py'),
               run_name='__main__')
