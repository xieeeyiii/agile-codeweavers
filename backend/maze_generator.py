import random
import constants as c

class MazeGenerator:
    @staticmethod
    def generate_maze(width=c.MAZE_DEFAULT_WIDTH, height=c.MAZE_DEFAULT_HEIGHT):
        """递归回溯法生成随机复杂迷宫"""
        # 1. 初始化全墙网格
        grid = [[c.WALL for _ in range(width)] for _ in range(height)]
        # 2. 起点（奇数坐标，保证路径连通）
        start_x, start_y = 1, 1
        grid[start_y][start_x] = c.FLOOR
        # 3. 递归回溯栈
        stack = [(start_x, start_y)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # 每次移动2格（跳过墙）

        while stack:
            current_x, current_y = stack[-1]
            random.shuffle(directions)  # 打乱方向增加随机性
            found = False

            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                # 边界检测+未访问检测
                if 0 < nx < width-1 and 0 < ny < height-1 and grid[ny][nx] == c.WALL:
                    # 挖通中间墙
                    grid[current_y + dy//2][current_x + dx//2] = c.FLOOR
                    grid[ny][nx] = c.FLOOR
                    stack.append((nx, ny))
                    found = True
                    break

            if not found:
                stack.pop()  # 回溯

        # 4. 随机放置物品（1-8个）和终点
        floor_cells = [(x, y) for y in range(height) for x in range(width) if grid[y][x] == c.FLOOR]
        random.shuffle(floor_cells)

        # 放置物品
        item_count = random.randint(1, min(8, len(floor_cells)//8))
        for _ in range(item_count):
            x, y = floor_cells.pop()
            grid[y][x] = c.ITEM

        # 放置终点
        if floor_cells:
            goal_x, goal_y = floor_cells.pop()
            grid[goal_y][goal_x] = c.GOAL

        # 5. 返回迷宫数据+玩家初始位置
        return {
            "grid": grid,
            "player_x": start_x,
            "player_y": start_y,
            "width": width,
            "height": height
        }