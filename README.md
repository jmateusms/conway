# Conway's game of life

This is an implementation of [Conway's game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python, using pygame for rendering.

![conway-demo](https://github.com/jmateusms/conway/assets/19481756/ac49dec5-5168-45c6-bced-9fb3537a125c)

There are two game modes:

## Conway simulation

Simulates Conway's game of life.

- You can click on cells to toggle them on or off.
- Pressing `space` advances the game by one step.
- Preesing `e` toggles auto-advancing the game.
- While auto-advancing, you can press the up/right arrow keys to increase the speed, and the down/left arrow keys to decrease the speed.

## Labyrinth game

Inspired by [SigmaGeek/Stone Automata Maze Challenge](https://sigmageek.com/stone_results/stone-automata-maze-challenge#!).

- Live cells are walls.
- The player is the red cell.
- The goal is the green cell.
- You can left-click on a cell to toggle it on or off.
- You can right-click on a cell to set it as the player or the goal.
- Walls are deadly, so don't touch them!

## Running

Tested on Python 3.10:

```bash
pip install -r requirements.txt
python main.py
```
