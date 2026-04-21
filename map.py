# map.py - 地图相关逻辑
import constants as c
import random

class MazeMap:
    def __init__(self, width=31, height=21):
        """
        初始化迷宫（默认31x21大型迷宫，宽高建议设为奇数，保证路径连通）
        :param width: 迷宫宽度（列数）
        :param height: 迷宫高度（行数）
        """
        # 覆盖常量的默认尺寸（适配动态迷宫）
        c.MAP_WIDTH = width
        c.MAP_HEIGHT = height
        
        # 随机生成复杂迷宫
        self.map_grid = self._generate_random_maze(width, height)
        # 随机放置物品和终点（保证不在墙上，且与玩家初始位置不重叠）
        self._place_random_items_and_goal()
        # 玩家初始位置（迷宫左上角安全区，避开边界墙）
        self.player_x = 1
        self.player_y = 1

    def _generate_random_maze(self, width, height):
        """递归回溯法生成随机迷宫（核心算法）"""
        # 1. 初始化网格：全墙（#），奇数行/列留作路径，偶数行/列留作墙
        grid = [[c.WALL for _ in range(width)] for _ in range(height)]
        # 2. 随机起点（必须是奇数坐标，保证路径连通）
        start_x = 1 if width > 2 else 0
        start_y = 1 if height > 2 else 0
        grid[start_y][start_x] = c.FLOOR
        # 3. 递归回溯挖路径
        stack = [(start_x, start_y)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # 每次移动2格（跳过墙）
        
        while stack:
            current_x, current_y = stack[-1]
            # 打乱方向，增加随机性
            random.shuffle(directions)
            found = False
            
            for dx, dy in directions:
                new_x = current_x + dx
                new_y = current_y + dy
                # 检查新坐标在边界内，且未被挖过
                if 0 < new_x < width-1 and 0 < new_y < height-1 and grid[new_y][new_x] == c.WALL:
                    # 挖通当前位置到新位置的墙（中间格）
                    grid[current_y + dy//2][current_x + dx//2] = c.FLOOR
                    grid[new_y][new_x] = c.FLOOR
                    stack.append((new_x, new_y))
                    found = True
                    break
            
            if not found:
                stack.pop()  # 回溯
        
        return grid

    def _place_random_items_and_goal(self):
        """随机放置物品（K）和终点（G），保证在地板上"""
        # 收集所有地板坐标
        floor_cells = []
        for y in range(c.MAP_HEIGHT):
            for x in range(c.MAP_WIDTH):
                if self.map_grid[y][x] == c.FLOOR:
                    floor_cells.append((x, y))
        
        if not floor_cells:
            return
        
        # 随机放置物品（至少1个）
        item_count = random.randint(1, min(5, len(floor_cells)//10))  # 按迷宫大小适配物品数量
        for _ in range(item_count):
            x, y = random.choice(floor_cells)
            self.map_grid[y][x] = c.ITEM
            floor_cells.remove((x, y))
        
        # 随机放置终点（保证与物品不重叠）
        if floor_cells:
            goal_x, goal_y = random.choice(floor_cells)
            self.map_grid[goal_y][goal_x] = c.GOAL

    def print_map(self):
        """打印当前地图（适配屏幕：紧凑显示 + 自动换行）"""
        print("\n===== 走迷宫游戏（按help查看操作） =====")
        # 获取终端宽度（适配不同屏幕）
        try:
            import os
            terminal_width = os.get_terminal_size().columns
            # 每个单元格占2字符（符号+空格），计算每行最多显示的列数
            max_cols_per_line = (terminal_width - 4) // 2  # 留4字符边距
        except:
            max_cols_per_line = c.MAP_WIDTH  # 兼容无终端环境
        
        # 分段打印地图（适配窄屏幕）
        for y in range(c.MAP_HEIGHT):
            row = ""
            printed_cols = 0
            for x in range(c.MAP_WIDTH):
                # 显示玩家/地图符号
                if x == self.player_x and y == self.player_y:
                    row += c.PLAYER + " "
                else:
                    row += self.map_grid[y][x] + " "
                printed_cols += 1
                # 达到屏幕宽度则换行
                if printed_cols >= max_cols_per_line and x < c.MAP_WIDTH - 1:
                    print(row)
                    row = ""
                    printed_cols = 0
            # 打印剩余列
            if row:
                print(row)
        print("=" * (min(c.MAP_WIDTH * 2, terminal_width) if 'terminal_width' in locals() else 20))

    def update_player_pos(self, new_x, new_y):
        """更新玩家位置（仅在合法移动时调用）"""
        self.player_x = new_x
        self.player_y = new_y

    def get_cell(self, x, y):
        """获取指定坐标的地图格子内容"""
        return self.map_grid[y][x]

    def set_cell(self, x, y, value):
        """修改指定坐标的地图格子内容（比如拾取物品后改地板）"""
        self.map_grid[y][x] = value