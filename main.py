# main.py - 游戏主入口（新手直接运行这个文件）
from map import MazeMap
from player import Player
from command import CommandHandler

def main():
    # 初始化游戏组件
    maze_map = MazeMap()
    player = Player()
    cmd_handler = CommandHandler(maze_map, player)

    # 欢迎信息
    print("🎉 欢迎来到走迷宫游戏！")
    print("💡 输入help查看操作说明，quit退出游戏。\n")

    # 游戏主循环（核心）
    while cmd_handler.game_running:
        # 打印当前地图
        maze_map.print_map()
        # 获取玩家输入
        user_input = input("请输入命令：")
        # 处理输入
        cmd_handler.process_input(user_input)

if __name__ == "__main__":
    main()