import requests
import time

BASE_URL = "http://localhost:5000"

def test_generate_maze():
    print("测试: 生成迷宫...")
    try:
        resp = requests.get(f"{BASE_URL}/api/generate-maze", timeout=10)
        assert resp.status_code == 200
        data = resp.json()
        assert "grid" in data
        print("✅ 迷宫生成测试通过")
        return True
    except Exception as e:
        print(f"❌ 迷宫生成测试失败: {e}")
        return False

def test_move():
    print("测试: 移动功能...")
    try:
        resp = requests.post(f"{BASE_URL}/api/move/w", timeout=10)
        assert resp.status_code in [200, 400]
        print("✅ 移动测试通过")
        return True
    except Exception as e:
        print(f"❌ 移动测试失败: {e}")
        return False

def test_reset():
    print("测试: 重置功能...")
    try:
        requests.get(f"{BASE_URL}/api/generate-maze")
        resp = requests.post(f"{BASE_URL}/api/reset", timeout=10)
        assert resp.status_code == 200
        print("✅ 重置测试通过")
        return True
    except Exception as e:
        print(f"❌ 重置测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 40)
    print("等待后端启动...")
    time.sleep(3)
    
    results = []
    results.append(test_generate_maze())
    results.append(test_move())
    results.append(test_reset())
    
    print("=" * 40)
    if all(results):
        print("✅ 所有测试通过")
        exit(0)
    else:
        print("❌ 部分测试失败")
        exit(1)