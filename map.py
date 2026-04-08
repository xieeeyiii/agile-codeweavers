# map.py - 地图相关逻辑
import constants as c

class MazeMap:
    def __init__(self):
        # 初始化5x5固定迷宫（MVP版本，新手易调试）
        # 布局说明：#=墙，.=地板，K=物品，G=终点
        self.map_grid = [
            [c.WALL, c.WALL, c.WALL, c.WALL, c.WALL],
            [c.WALL, c.FLOOR, c.ITEM, c.FLOOR, c.WALL],
            [c.WALL, c.FLOOR, c.WALL, c.FLOOR, c.WALL],
            [c.WALL, c.FLOOR, c.FLOOR, c.GOAL, c.WALL],
            [c.WALL, c.WALL, c.WALL, c.WALL, c.WALL]
        ]
        # 记录玩家初始位置（第二行第二列，索引从0开始）
        self.player_x = 1
        self.player_y = 1

    def print_map(self):
        """打印当前地图（包含玩家位置）"""
        print("\n===== 走迷宫游戏 =====")
        for y in range(c.MAP_HEIGHT):
            row = ""
            for x in range(c.MAP_WIDTH):
                # 如果当前位置是玩家，显示玩家符号，否则显示地图原有符号
                if x == self.player_x and y == self.player_y:
                    row += c.PLAYER + " "
                else:
                    row += self.map_grid[y][x] + " "
            print(row)
        print("======================\n")

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