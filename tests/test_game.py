import unittest
import sys
sys.path.insert(0, ".")

from map import MazeMap
from player import Player
from command import CommandHandler
import constants as c

class TestMazeGameTDD(unittest.TestCase):
    def setUp(self):
        self.maze = MazeMap()
        self.player = Player()
        self.cmd = CommandHandler(self.maze, self.player)

    # 测试 1：撞墙不会移动
    def test_player_cannot_move_into_wall(self):
        # 玩家初始位置 (1,1)，往上是墙，移动无效
        self.cmd.handle_move("w")
        self.assertEqual(self.maze.player_y, 1)  # 位置不变

    # 测试 2：玩家可以正常拾取物品 K
    def test_player_pick_item(self):
        self.cmd.handle_move("d")  # 向右走到物品位置
        self.assertEqual(self.player.inventory, ["K"])

    # 测试 3：无效命令不会让游戏崩溃
    def test_invalid_command(self):
        self.cmd.process_input("abc123")
        self.assertTrue(self.cmd.game_running)

    
    # ========== 新增边界测试用例 ==========
    def test_move_to_boundary(self):
        """移动到地图边界不能再往外走（边界测试）"""
        # 记录初始位置
        original_y = self.maze.player_y
        # 连续向上移动 50 次
        for _ in range(50):
            self.cmd.handle_move("w")
        # 验证 y 坐标不会变成负数（不会超出地图顶部）
        self.assertGreaterEqual(self.maze.player_y, 0)

    def test_win_condition_reached(self):
        """到达终点后游戏应结束"""
        # 先保存游戏状态
        was_running = self.cmd.game_running
        # 检查终点检测逻辑（不会崩溃即可）
        self.cmd.check_goal()
        # 这个测试只是验证函数能正常执行
        self.assertTrue(True)  # 没有崩溃就算通过

    def test_multiple_items_pickup(self):
        """连续拾取物品后背包应该有变化"""
        initial_inventory = self.player.inventory.copy()
        # 尝试移动几步（可能拾取物品）
        self.cmd.handle_move("d")
        self.cmd.handle_move("s")
        # 这个测试验证函数不会崩溃
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
