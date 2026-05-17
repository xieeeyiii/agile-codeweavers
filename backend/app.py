# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random

WALL = '#'
FLOOR = '.'
ITEM = '🔑'
GOAL = '🚩'
MAZE_WIDTH = 31
MAZE_HEIGHT = 21

app = Flask(__name__, static_folder='../frontend')
CORS(app)

current_maze = None
keys_collected = 0

def generate_maze():
    """生成随机迷宫"""
    global current_maze, keys_collected
    
    width, height = MAZE_WIDTH, MAZE_HEIGHT
    grid = [[WALL for _ in range(width)] for _ in range(height)]
    start_x, start_y = 1, 1
    grid[start_y][start_x] = FLOOR
    stack = [(start_x, start_y)]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        cx, cy = stack[-1]
        random.shuffle(directions)
        found = False
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < width-1 and 0 < ny < height-1 and grid[ny][nx] == WALL:
                grid[cy + dy//2][cx + dx//2] = FLOOR
                grid[ny][nx] = FLOOR
                stack.append((nx, ny))
                found = True
                break
        if not found:
            stack.pop()

    # 收集地板格子
    floors = [(x, y) for y in range(height) for x in range(width) if grid[y][x] == FLOOR]
    random.shuffle(floors)

    # 放置钥匙
    key_count = random.randint(3, 8)
    for _ in range(min(key_count, len(floors))):
        if floors:
            x, y = floors.pop()
            grid[y][x] = ITEM

    # 放置终点
    if floors:
        x, y = floors.pop()
        grid[y][x] = GOAL

    current_maze = {
        "grid": grid,
        "player_x": start_x,
        "player_y": start_y,
        "width": width,
        "height": height,
        "total_keys": key_count
    }
    keys_collected = 0
    return current_maze

# ========== API 路由（必须放在最前面） ==========
@app.route('/api/generate-maze', methods=['GET'])
def api_generate_maze():
    maze = generate_maze()
    return jsonify({**maze, "keys_collected": keys_collected})

@app.route('/api/move/<direction>', methods=['POST', 'GET'])
def api_move_player(direction):
    global current_maze, keys_collected
    
    if not current_maze:
        return jsonify({"error": "请先生成迷宫"}), 400
    
    px, py = current_maze["player_x"], current_maze["player_y"]
    nx, ny = px, py
    
    if direction == 'w': ny -= 1
    elif direction == 's': ny += 1
    elif direction == 'a': nx -= 1
    elif direction == 'd': nx += 1
    else:
        return jsonify({"error": "无效方向"}), 400
    
    if nx < 0 or nx >= current_maze["width"] or ny < 0 or ny >= current_maze["height"]:
        return jsonify({"success": False, "message": "不能走出边界！"})
    
    cell = current_maze["grid"][ny][nx]
    
    if cell == WALL:
        return jsonify({"success": False, "message": "撞墙了！"})
    
    # 执行移动
    current_maze["player_x"], current_maze["player_y"] = nx, ny
    
    response = {
        "success": True,
        "player_x": nx,
        "player_y": ny,
        "cell": cell,
        "keys_collected": keys_collected,
        "total_keys": current_maze["total_keys"]
    }
    
    if cell == ITEM:
        keys_collected += 1
        current_maze["grid"][ny][nx] = FLOOR
        response["message"] = f"拾取钥匙！({keys_collected}/{current_maze['total_keys']})"
        response["keys_collected"] = keys_collected
    
    elif cell == GOAL:
        if keys_collected >= current_maze["total_keys"]:
            response["message"] = "胜利！通关成功！"
            response["victory"] = True
        else:
            need = current_maze["total_keys"] - keys_collected
            response["message"] = f"需要集齐所有钥匙！还需{need}把"
    
    return jsonify(response)

@app.route('/api/reset', methods=['POST'])
def api_reset():
    global keys_collected
    if current_maze:
        keys_collected = 0
        current_maze["player_x"], current_maze["player_y"] = 1, 1
        return jsonify({"success": True, "message": "游戏已重置"})
    return jsonify({"error": "无游戏"}), 400

# ========== 静态文件路由（放在最后） ==========
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    # 如果路径以 api/ 开头，说明是API请求被误匹配了
    if path.startswith('api/'):
        return jsonify({"error": "API endpoint not found"}), 404
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    print("🎮 迷宫游戏后端启动中...")
    print("📍 访问地址: http://127.0.0.1:5000")
    print("📍 API文档: http://127.0.0.1:5000/api/generate-maze")
    app.run(host='0.0.0.0', port=5000, debug=True)