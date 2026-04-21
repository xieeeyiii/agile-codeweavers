# CodeWeavers

## 团队口号
Weaving code into solutions

---

## 团队成员与Scrum角色

| 序号 | 姓名 | 学号 | 角色 |
|:---:|:------|:---------|:---------------------|
| 1 | 谢依 | 9109223144 | Scrum Master (SM) |
| 2 | 郑淑婷 | 7803123141 | 产品负责人 (PO) |
| 3 | 徐雨萱 | 9109223139 | 开发团队 (Dev Team) |

> **说明**：在Scrum中，Scrum Master和产品负责人同时也是开发团队的成员，三人共同组成完整的开发团队，对所有交付成果负责。

---

## 关于我们

CodeWeavers是一支由AI赋能的敏捷开发小队，致力于用Scrum方法论和AI编程工具，将每一行代码编织成优雅的解决方案。

## 系统架构
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   前端页面   │ ←→ │ Flask 后端  │ ←→ │ 游戏核心模块 │
│ index.html  │    │ app.py      │    │ map/player/ │
│ script.js   │    │ openapi.yaml│    │ command     │
│ style.css   │    │             │    │ constants   │
└─────────────┘     └─────────────┘     └─────────────┘

## 本地开发环境搭建
1. 克隆/下载项目代码
2. 安装 Python 3.8+
3. 安装依赖：
   pip install flask flask-cors flask-swagger-ui
4. 启动后端：
   python app.py
5. 打开浏览器访问：
   http://127.0.0.1:5000
6. API 文档地址：
   http://127.0.0.1:5000/api-docs


## 核心模块职责
- app.py：Flask 后端入口，提供迷宫生成、玩家移动 API
- player.py：玩家背包、物品拾取逻辑
- map.py：迷宫生成、地图渲染、玩家位置管理
- command.py：命令解析、移动逻辑
- constants.py：游戏符号、常量统一管理
- index.html / script.js / style.css：前端页面与交互
- openapi.yaml：API 接口文档定义
