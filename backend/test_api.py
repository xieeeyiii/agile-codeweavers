import pytest
import requests

BASE_URL = "http://localhost:5000"

class TestMazeAPI:
    
    def test_generate_maze(self):
        """测试迷宫生成"""
        resp = requests.get(f"{BASE_URL}/api/generate-maze")
        assert resp.status_code == 200
        data = resp.json()
        assert "grid" in data
        print("✅ 迷宫生成测试通过")
    
    def test_move_invalid_direction(self):
        """测试无效方向"""
        requests.get(f"{BASE_URL}/api/generate-maze")
        resp = requests.post(f"{BASE_URL}/api/move/x")
        assert resp.status_code == 400
        print("✅ 无效方向测试通过")
    
    def test_reset_game(self):
        """测试重置功能"""
        requests.get(f"{BASE_URL}/api/generate-maze")
        resp = requests.post(f"{BASE_URL}/api/reset")
        assert resp.status_code == 200
        print("✅ 重置游戏测试通过")