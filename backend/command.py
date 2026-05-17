# command.py - 命令解析逻辑
import constants as c

class CommandHandler:
    def __init__(self, maze_map, player):
        self.maze_map = maze_map
        self.player = player
        self.game_running = True  # 控制游戏主循环

    def process_input(self, user_input):
        """处理玩家输入（核心函数）"""
        # 标准化输入：转小写+去掉前后空格（避免玩家输入W、 w、W 等情况）
        cmd = user_input.strip().lower()

        # 空输入直接返回
        if not cmd:
            print("⚠️ 请输入有效命令！输入help查看操作说明。")
            return

        # 处理移动命令
        if cmd in [c.MOVE_UP, c.MOVE_LEFT, c.MOVE_DOWN, c.MOVE_RIGHT]:
            self.handle_move(cmd)
        # 处理功能命令
        elif cmd == c.CMD_HELP:
            self.show_help()
        elif cmd == c.CMD_INVENTORY:
            self.player.show_inventory()
        elif cmd == c.CMD_QUIT:
            self.game_running = False
            print("👋 游戏退出，再见！")
        # 无效命令
        else:
            print(f"❌ 未知命令：{cmd}！输入help查看操作说明。")

    def handle_move(self, direction):
        """处理移动逻辑（核心：边界+撞墙检测）"""
        # 获取当前玩家位置
        current_x = self.maze_map.player_x
        current_y = self.maze_map.player_y

        # 计算新位置
        new_x, new_y = current_x, current_y
        if direction == c.MOVE_UP:
            new_y -= 1
        elif direction == c.MOVE_LEFT:
            new_x -= 1
        elif direction == c.MOVE_DOWN:
            new_y += 1
        elif direction == c.MOVE_RIGHT:
            new_x += 1

        # 1. 边界检测（新手必做：避免索引越界崩溃）
        if (new_x < 0 or new_x >= c.MAP_WIDTH) or (new_y < 0 or new_y >= c.MAP_HEIGHT):
            print("🚫 不能走出地图边界！")
            return

        # 2. 撞墙检测
        cell_content = self.maze_map.get_cell(new_x, new_y)
        if cell_content == c.WALL:
            print("🚫 撞到墙了！")
            return

        # 3. 合法移动：更新玩家位置
        self.maze_map.update_player_pos(new_x, new_y)

        # 4. 拾取物品检测
        if cell_content == c.ITEM:
            self.player.pick_item(cell_content)
            # 拾取后把物品位置改成地板
            self.maze_map.set_cell(new_x, new_y, c.FLOOR)

        # 5. 到达终点检测（游戏胜利）
        if cell_content == c.GOAL:
            print("🎉 恭喜你到达终点，游戏胜利！")
            self.game_running = True  # 这里设为False会直接退出，新手可以先设为True继续玩

    def show_help(self):
        """显示帮助说明"""
        print("📋 操作说明：")
        print("  移动：w(上)、a(左)、s(下)、d(右)")
        print("  功能：")
        print("    help - 查看本说明")
        print("    inventory - 查看背包")
        print("    quit - 退出游戏")