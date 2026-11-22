# CS188 Final Project

Team project based on **CS188: Introduction to Artificial Intelligence** (UC Berkeley, Spring 2026).
Original assignments: <https://inst.eecs.berkeley.edu/~cs188/sp26/projects/>

This repository covers Projects 1, 2, 3 and 5.

## Structure

| Folder | Project | Topics |
|---|---|---|
| `proj1-search/` | Project 1 – Search | DFS, BFS, UCS, A*, heuristics |
| `proj2-multiagent/` | Project 2 – Multi-Agent Search | Reflex agent, Minimax, Alpha-Beta, Expectimax |
| `proj3-rl/` | Project 3 – Reinforcement Learning | Value Iteration, Q-Learning, Approximate Q-Learning |
| `proj5-ml/` | Project 5 – Machine Learning | Perceptron, neural networks, RNN, CNN, attention (PyTorch) |
| `docs/` | – | Reports and shared documents |

## Getting started

Clone the repository:

```bash
git clone https://github.com/VTongg159/cs188-final.git
cd cs188-final
```

## Workflow

- Work on a branch for your project: `proj1`, `proj2` or `proj3`. Do not commit directly to `main`.
- Merge into `main` through a Pull Request, then delete the branch so the repository keeps only `main`.
- Prefix commit messages with the project: `p1: ...`, `p2: ...`, `p3: ...`.
  Shared changes (README, docs, config) use `docs: ...` or `chore: ...`.
- Only edit your own project folder.
- The first commit of each project is the unmodified starter code, so later diffs show only our changes:
  download the project zip from the course website and extract its files directly into the project folder
  (e.g. `proj1-search/search.py`, not `proj1-search/search/search.py`), then commit it as `pX: add original starter code`.

```bash
git checkout main && git pull
git checkout -b proj1          # first time; afterwards: git checkout proj1
# ...add starter code, edit code...
git add proj1-search/
git commit -m "p1: ..."
git push -u origin proj1
gh pr create --base main --head proj1   # or open the Pull Request on GitHub
# after the PR is merged: delete the branch (button on the PR page)
git checkout main && git pull && git branch -d proj1
```

## Environment

```bash
conda create -n cs188 python=3.10 -y
conda activate cs188
pip install "numpy<2.0" matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cpu   # required for Project 5
```

## Running the autograder

```bash
cd projX-...
python autograder.py                  # all questions
python autograder.py -q q1            # a single question
python autograder.py --no-graphics    # without visualizations
```

Project 5 dependency check: `cd proj5-ml && python autograder.py --check-dependencies`
