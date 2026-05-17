# Maze Game - AGENTS.md
## 1. Project Architecture
Python console maze game with modular separation: main loop, map system, player system, command processing, and constant definitions.

## 2. Directory Structure
main.py       Game entry and main loop
map.py        Map rendering, position, cell operations
player.py     Player inventory and item pickup
command.py    Input handling and movement validation
constants.py  Global constants and game symbols

## 3. Core Responsibilities
MazeMap: Render map, manage player position, check walls/bounds
Player: Manage inventory, collect items
CommandHandler: Process input, validate movement, detect goal
constants: Store all fixed values to avoid hardcoding

## 4. Coding Rules
Class names: PascalCase
Functions: camelCase
Movement requires boundary + wall checks
Use constants instead of hardcoded values

## 5. Forbidden Actions
Do NOT modify map_grid directly
Do NOT hardcode game symbols (e.g., '#', '@')
Do NOT mix rendering logic into command handling
Do NOT move player without collision checks
