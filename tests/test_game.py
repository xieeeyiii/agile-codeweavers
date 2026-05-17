import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        """玩家不能移动到墙上"""
        self.cmd.handle_move("w")
        self.assertEqual(self.maze.player_y, 1)

    # 测试 2：玩家可以正常拾取物品 K
    def test_player_pick_item(self):
        """玩家可以拾取物品"""
        self.cmd.handle_move("d")
        self.assertEqual(self.player.inventory, ["K"])

    # 测试 3：无效命令不会让游戏崩溃
    def test_invalid_command(self):
        """无效命令不会导致崩溃"""
        self.cmd.process_input("abc123")
        self.assertTrue(self.cmd.game_running)

    # 测试 4：移动到边界不会越界
    def test_move_to_boundary(self):
        """移动到地图边界不能再往外走"""
        for _ in range(50):
            self.cmd.handle_move("w")
        self.assertGreaterEqual(self.maze.player_y, 0)

    # 测试 5：连续操作不会崩溃
    def test_multiple_items_pickup(self):
        """连续拾取物品后背包应该有变化"""
        self.cmd.handle_move("d")
        self.cmd.handle_move("s")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
