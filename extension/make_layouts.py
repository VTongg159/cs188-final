"""Builds the two large layouts of the extension scenario (fixed seeds, reproducible).

    python3 extension/make_layouts.py

layouts/mudMaze.lay   61 x 41 maze with loops; '~' marks mud cells (cost 5 per step).
                      Pacman starts top-left, the single food is the goal (bottom-right).
                      The layout reader ignores '~', so the file also opens in pacman.py.
layouts/bigArena.lay  41 x 23 braided maze (no dead ends) full of food, 4 capsules,
                      3 ghosts in the middle, Pacman at the bottom.
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'layouts')


def maze(cells_w, cells_h, seed, loops, braid=False):
    """Recursive-backtracker maze on a (2w+1) x (2h+1) character grid, then extra
    walls are removed: a share `loops` of the remaining inner walls, and with
    braid=True every dead end is opened too."""
    rng = random.Random(seed)
    W, H = 2 * cells_w + 1, 2 * cells_h + 1
    g = [['%'] * W for _ in range(H)]
    stack, seen = [(0, 0)], {(0, 0)}
    g[1][1] = ' '
    while stack:
        cx, cy = stack[-1]
        options = [(cx + dx, cy + dy, dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= cx + dx < cells_w and 0 <= cy + dy < cells_h and (cx + dx, cy + dy) not in seen]
        if not options:
            stack.pop()
            continue
        nx, ny, dx, dy = rng.choice(options)
        g[2 * cy + 1 + dy][2 * cx + 1 + dx] = ' '
        g[2 * ny + 1][2 * nx + 1] = ' '
        seen.add((nx, ny))
        stack.append((nx, ny))
    inner = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1)
             if g[y][x] == '%' and (x % 2) != (y % 2)]          # walls between two cells
    for x, y in rng.sample(inner, int(loops * len(inner))):
        g[y][x] = ' '
    if braid:
        for y in range(1, H, 2):
            for x in range(1, W, 2):
                walls = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                         if 0 < x + dx < W - 1 and 0 < y + dy < H - 1 and g[y + dy][x + dx] == '%']
                open_sides = 4 - sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                                     if g[y + dy][x + dx] == '%')
                if open_sides == 1 and walls:
                    wx, wy = rng.choice(walls)
                    g[wy][wx] = ' '
    return g


def write(name, g):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w') as f:
        f.write('\n'.join(''.join(row) for row in g) + '\n')


# Scenario A: mud maze ---------------------------------------------------------------
g = maze(30, 20, seed=188, loops=0.12)
H, W = len(g), len(g[0])
rng = random.Random(7)
for _ in range(9):                                     # nine rectangular mud zones
    w, h = rng.randint(6, 14), rng.randint(4, 9)
    x0, y0 = rng.randint(1, W - w - 1), rng.randint(1, H - h - 1)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if g[y][x] == ' ':
                g[y][x] = '~'
g[1][1] = 'P'                                           # top-left
g[H - 2][W - 2] = '.'                                   # bottom-right: the goal
write('mudMaze.lay', g)

# Scenario B: big arena ----------------------------------------------------------------
g = maze(20, 11, seed=2026, loops=0.15, braid=True)
H, W = len(g), len(g[0])
for y in range(1, H - 1):
    for x in range(1, W - 1):
        if g[y][x] == ' ':
            g[y][x] = '.'
cy, cx = H // 2, W // 2
for x in range(cx - 3, cx + 4):                        # ghost house: open row in the middle
    g[cy][x] = ' '
g[cy][cx - 2], g[cy][cx], g[cy][cx + 2] = 'G', 'G', 'G'
for x, y in [(1, 1), (W - 2, 1), (1, H - 2), (W - 2, H - 2)]:
    g[y][x] = 'o'
g[H - 2][cx] = 'P'
write('bigArena.lay', g)
print(open(os.path.join(OUT, 'mudMaze.lay')).read())
print(open(os.path.join(OUT, 'bigArena.lay')).read())
