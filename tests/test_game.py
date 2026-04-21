import unittest
import sys
sys.path.append("..")  

from map import MazeMap
from player import Player
from command import CommandHandler

class TestMazeGame(unittest.TestCase):
    def setUp(self):
        self.maze = MazeMap()
        self.player = Player()
        self.cmd_handler = CommandHandler(self.maze, self.player)

    # 测试1：玩家不能越界
    def test_move_out_of_border(self):
        self.cmd_handler.handle_move("w")
        self.cmd_handler.handle_move("w")
        self.assertEqual(self.maze.player_y, 0)

    # 测试2：能正常拾取物品
    def test_pick_item(self):
        self.cmd_handler.handle_move("d")
        self.assertEqual(self.player.inventory, ["K"])

    # 测试3：无效命令不崩溃
    def test_invalid_command(self):
        self.cmd_handler.process_input("invalid")
        self.assertTrue(self.cmd_handler.game_running)

if __name__ == '__main__':
    unittest.main()
