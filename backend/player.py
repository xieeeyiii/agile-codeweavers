# player.py - 玩家相关逻辑
import constants as c

class Player:
    def __init__(self):
        self.inventory = []  # 玩家背包，初始为空

    def pick_item(self, item):
        """拾取物品（添加到背包，并去重）"""
        if item not in self.inventory:
            self.inventory.append(item)
            print(f"✅ 拾取了{item}！")

    def show_inventory(self):
        """显示背包内容"""
        if self.inventory:
            print(f"🎒 你的背包：{', '.join(self.inventory)}")
        else:
            print("🎒 你的背包是空的！")