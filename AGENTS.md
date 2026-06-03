# Maze Game - AGENTS.md

## 1. Project Architecture
Python console maze game with modular separation: main loop, map system, player system, command processing, and constant definitions.

## 2. Directory Structure
main.py       Game entry and main loop
map.py        Map rendering, position, cell operations
player.py     Player inventory and item pickup
command.py    Input handling and movement validation
constants.py  Global constants and game symbols
tests/        Unit tests for core modules

## 3. Core Responsibilities
| Module | Responsibility |
|--------|----------------|
| MazeMap | Render map, manage player position, check walls/bounds |
| Player | Manage inventory, collect items |
| CommandHandler | Process input, validate movement, detect goal |
| constants | Store all fixed values to avoid hardcoding |

## 4. Coding Rules
- Class names: `PascalCase`
- Functions: `camelCase`
- Movement requires boundary + wall checks
- Use constants instead of hardcoded values (e.g., use `c.WALL` instead of `'#'`)

## 5. Forbidden Actions
- Do NOT modify `map_grid` directly
- Do NOT hardcode game symbols (e.g., '#', '@')
- Do NOT mix rendering logic into command handling
- Do NOT move player without collision checks

## 6. Data Flow
Game execution order:

1. main.py starts game loop
   - while game_running:
     - get user input -> CommandHandler.process_input()

2. CommandHandler.process_input() parses input
   - if "w/a/s/d" -> handle_move()
   - if "help" -> show help text
   - if "quit" -> exit game
   - else -> "unknown command"

3. handle_move() movement logic:
   - Calculate new position based on direction
   - MazeMap.is_wall() -> check if new position is wall
   - if wall -> print error, no position change
   - if not wall -> MazeMap.update_position()

4. After movement, item pickup check:
   - MazeMap.get_cell_type() at new position
   - if cell is item ('K', 'L', etc.) -> Player.add_to_inventory()
   - MazeMap.clear_item() -> remove item from map

5. Goal detection:
   - If current position == goal position ('G')
   - game_running = False -> exit game loop

Key dependencies:
- command.py imports: map.py, player.py, constants.py
- map.py imports: constants.py only
- player.py imports: constants.py only
- main.py imports: command.py, map.py, player.py, constants.py

## 7. Key Functions Reference
| Function | Location | Description |
|----------|----------|-------------|
| handle_move(direction) | command.py | Move player if valid direction |
| is_wall(x, y) | map.py | Check if cell is a wall |
| update_position(x, y) | map.py | Set new player position |
| add_to_inventory(item) | player.py | Add item to player's inventory |
| process_input(user_input) | command.py | Parse and route user commands |

## 8. Example: How to add a new item type
1. Add new symbol in `constants.py` (e.g., `POTION = 'P'`)
2. Update `Player.add_to_inventory()` to handle new item
3. Place item on map in `map.py` initialization
4. No changes needed to command.py or main.py

## 9. Testing
Run unit tests：
```bash
python -m unittest tests/test_game.py
Or with pytest:
pytest tests/test_game.py -v
