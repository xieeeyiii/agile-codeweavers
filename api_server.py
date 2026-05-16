# 后端接口服务
from flask import Flask, jsonify, request
from flask_cors import CORS
from map import MazeMap
from player import Player
from command import CommandHandler

app = Flask(__name__)
CORS(app)

# 初始化游戏
maze_map = MazeMap()
player = Player()
cmd_handler = CommandHandler(maze_map, player)

@app.route('/api/game/init', methods=['GET'])
def game_init():
    return jsonify({
        "map": maze_map.map_grid,
        "player": {"x": maze_map.player_x, "y": maze_map.player_y},
        "inventory": player.inventory
    })

@app.route('/api/game/command', methods=['POST'])
def game_command():
    data = request.get_json()
    cmd = data.get("cmd", "")
    cmd_handler.process_input(cmd)

    return jsonify({
        "player": {"x": maze_map.player_x, "y": maze_map.player_y},
        "inventory": player.inventory,
        "map": maze_map.map_grid
    })

@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    global maze_map, player, cmd_handler
    maze_map = MazeMap()
    player = Player()
    cmd_handler = CommandHandler(maze_map, player)
    return jsonify({"status": "reset_success"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
