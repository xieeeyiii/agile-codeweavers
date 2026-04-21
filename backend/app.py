from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import random
import os
# ---------------------- 常量定义 ----------------------
WALL = '#'
FLOOR = '.'
ITEM = '🔑'
GOAL = '🚩'
MAZE_DEFAULT_WIDTH = 41
MAZE_DEFAULT_HEIGHT = 21

# ---------------------- 迷宫生成器 ----------------------
class MazeGenerator:
    @staticmethod
    def generate_maze(width=MAZE_DEFAULT_WIDTH, height=MAZE_DEFAULT_HEIGHT):
        grid = [[WALL for _ in range(width)] for _ in range(height)]
        start_x, start_y = 1, 1
        grid[start_y][start_x] = FLOOR
        stack = [(start_x, start_y)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            current_x, current_y = stack[-1]
            random.shuffle(directions)
            found = False
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 < nx < width-1 and 0 < ny < height-1 and grid[ny][nx] == WALL:
                    grid[current_y + dy//2][current_x + dx//2] = FLOOR
                    grid[ny][nx] = FLOOR
                    stack.append((nx, ny))
                    found = True
                    break
            if not found:
                stack.pop()

        floor_cells = [(x, y) for y in range(height) for x in range(width) if grid[y][x] == FLOOR]
        random.shuffle(floor_cells)

        # 放置物品
        item_count = random.randint(1, min(8, len(floor_cells)//8))
        for _ in range(item_count):
            if floor_cells:
                x, y = floor_cells.pop()
                grid[y][x] = ITEM

        # 放置终点
        if floor_cells:
            goal_x, goal_y = floor_cells.pop()
            grid[goal_y][goal_x] = GOAL

        return {
            "grid": grid,
            "player_x": start_x,
            "player_y": start_y,
            "width": width,
            "height": height
        }

# ---------------------- Flask服务 ----------------------
# 关键：设置静态文件目录为前端文件夹
app = Flask(
    __name__,
    static_folder="../frontend",  # 确保这里的路径正确
    static_url_path=""  # 让静态文件路由不影响API
)
CORS(app, supports_credentials=True)
current_maze = None

# 【必须】API路由写在最前面，优先级最高
@app.route("/api/generate-maze", methods=["GET"])
def generate_maze():
    global current_maze
    current_maze = MazeGenerator.generate_maze()
    return jsonify(current_maze)

@app.route("/api/move-player/<direction>", methods=["GET"])

def move_player(direction):
    if not current_maze:
        return jsonify({"error": "未生成迷宫"}), 400

    px, py = current_maze["player_x"], current_maze["player_y"]
    nx, ny = px, py

    if direction == "w": ny -= 1
    elif direction == "a": nx -= 1
    elif direction == "s": ny += 1
    elif direction == "d": nx += 1
    else:
        return jsonify({"error": "无效方向"}), 400

    if nx < 0 or nx >= current_maze["width"] or ny < 0 or ny >= current_maze["height"]:
        return jsonify({"success": False, "msg": "超出边界"})

    cell = current_maze["grid"][ny][nx]
    if cell == WALL:
        return jsonify({"success": False, "msg": "撞到墙了"})

    current_maze["player_x"], current_maze["player_y"] = nx, ny
    result = {
        "success": True,
        "player_x": nx,
        "player_y": ny,
        "cell": cell
    }

    if cell == ITEM:
        current_maze["grid"][ny][nx] = FLOOR
        result["msg"] = "拾取了钥匙！"
    elif cell == GOAL:
        result["msg"] = "恭喜到达终点！"
        result["goal"] = True

    return jsonify(result)

# ==============================================================================
# SWAGGER API DOCS (MOCK环境测试页面)
# ==============================================================================
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api-docs"
API_URL = "/openapi.yaml"

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Maze Game API"
    }
)
app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

@app.route("/openapi.yaml")
def openapi_yaml():
    return send_from_directory("..", "openapi.yaml")
# 【必须】静态文件路由放在最后，并且用send_static_file而不是通用path路由
@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:filename>")
def static_files(filename):
    # 排除API路径，防止误匹配
    if filename.startswith("api/"):
        return "Not Found", 404
    return app.send_static_file(filename)

if __name__ == "__main__":
    # 验证静态文件目录是否存在
    print("当前工作目录:", os.getcwd())
    print("静态文件目录:", os.path.abspath(app.static_folder))
    app.run(debug=True, host="0.0.0.0", port=5000)

