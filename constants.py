# constants.py - 游戏常量定义（所有固定值都放这里）
# 地图符号
WALL = '#'          # 墙
FLOOR = '.'         # 地板
PLAYER = '@'        # 玩家
ITEM = 'K'          # 物品（钥匙）
GOAL = 'G'          # 终点

# 移动命令（小写，方便统一处理）
MOVE_UP = 'w'
MOVE_LEFT = 'a'
MOVE_DOWN = 's'
MOVE_RIGHT = 'd'

# 功能命令
CMD_HELP = 'help'   # 查看帮助
CMD_INVENTORY = 'inventory'  # 查看背包
CMD_QUIT = 'quit'   # 退出游戏

# 地图尺寸（MVP用5x5，新手易调试）
MAP_WIDTH = 5
MAP_HEIGHT = 5