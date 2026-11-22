# Extension: larger scenarios

The techniques of Projects 1-3 applied unchanged to two larger, generated maps.

| File | Content |
|---|---|
| `make_layouts.py` | Builds `layouts/mudMaze.lay` (61x41 maze, `~` = mud, cost 5) and `layouts/bigArena.lay` (41x23, 472 food, 3 ghosts) |
| `run_extension.py` | All experiments; prints the tables and writes `results.json` (about 5 min, 18 processes) |
| `results.json` | Results used in the report |

```bash
python3 extension/make_layouts.py
python3 extension/run_extension.py
python3 run.py -l extension/layouts/bigArena.lay -p ExpectimaxAgent -a evalFn=better,depth=2
```
