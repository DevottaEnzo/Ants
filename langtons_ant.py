#!/usr/bin/env python3
"""Langton's Ant -> PNG.

Usage examples:
  python langtons_ant.py                          # classic ant (rule RL), 12000 steps
  python langtons_ant.py -s 200000 -g 400 -o ant.png
  python langtons_ant.py --rule RLR -s 500000     # multi-colour "turmite" variants
  python langtons_ant.py --rule LLRR --scale 2

Rule string: one letter per colour. R = turn right, L = turn left.
The classic ant is "RL" (white cell -> turn right, black cell -> turn left).
Requires: pip install pillow
"""
import argparse
from PIL import Image

# Palette: index 0 is the background. Extra colours are used for longer rules.
PALETTE = [
    (255, 255, 255), (20, 20, 20), (220, 60, 60), (60, 140, 230),
    (80, 190, 110), (240, 190, 50), (150, 90, 200), (60, 200, 200),
]


def simulate(size, steps, rule):
    n = len(rule)
    grid = bytearray(size * size)          # cell colour indices
    x = y = size // 2
    dx, dy = 0, -1                         # facing up
    turn_right = [c.upper() == "R" for c in rule]

    for _ in range(steps):
        i = y * size + x
        c = grid[i]
        # turn: right (clockwise) or left (counter-clockwise)
        dx, dy = (-dy, dx) if turn_right[c] else (dy, -dx)
        # flip/advance colour, then move (torus wrap-around)
        grid[i] = (c + 1) % n
        x = (x + dx) % size
        y = (y + dy) % size
    return grid, (x, y)


def render(grid, size, scale, rule, show_ant=None):
    img = Image.frombytes("P", (size, size), bytes(grid))
    flat = [v for col in PALETTE[: max(len(rule), 2)] for v in col]
    img.putpalette(flat)
    img = img.convert("RGB")
    if show_ant:
        img.putpixel(show_ant, (255, 0, 0))
    if scale > 1:
        img = img.resize((size * scale, size * scale), Image.NEAREST)
    return img


def main():
    p = argparse.ArgumentParser(description="Langton's Ant PNG generator")
    p.add_argument("-s", "--steps", type=int, default=12000)
    p.add_argument("-g", "--grid", type=int, default=200, help="grid size (square)")
    p.add_argument("--scale", type=int, default=4, help="pixels per cell")
    p.add_argument("--rule", default="RL", help="e.g. RL (classic), RLR, LLRR")
    p.add_argument("--ant", action="store_true", help="mark final ant position in red")
    p.add_argument("-o", "--output", default="langtons_ant.png")
    a = p.parse_args()

    if not a.rule or set(a.rule.upper()) - {"L", "R"} or len(a.rule) < 2:
        p.error("--rule must be 2+ letters of L/R, e.g. RL")
    if len(a.rule) > len(PALETTE):
        p.error(f"--rule max length is {len(PALETTE)}")

    grid, pos = simulate(a.grid, a.steps, a.rule)
    img = render(grid, a.grid, a.scale, a.rule, pos if a.ant else None)
    img.save(a.output)
    print(f"Saved {a.output} ({img.width}x{img.height}px, {a.steps} steps, rule {a.rule.upper()})")


if __name__ == "__main__":
    main()
