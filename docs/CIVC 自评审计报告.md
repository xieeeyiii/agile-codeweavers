# <center>CIVC 自评审计报告</center>

## 项目定位

本报告针对“迷宫游戏”Python 控制台项目，参照 CIVC 四阀门框架，对其在 AI 辅助开发场景下的工程准备度进行自评审计。报告涵盖：AI 可访问文件的约束管理、AI 理解项目所需的上下文信息、AI 生成代码的自动化验证机制、以及错误代码的一键回滚能力。每个阀门均包含“当前状态”与“具体改进方案”，薄弱环节已落地改进方案并附证据占位符。

---

## 审计阀门一：约束（Constraint）

**目标**：明确 AI 能访问/修改哪些文件，实现沙盒隔离。

### 当前状态

- 项目根目录**存在** `.aiignore` 文件，用于限制 AI 助手直接修改核心配置与文档。
- 该文件明确列出禁止 AI 修改的文件清单：
  - `constants.py` —— 全局常量，改动可能导致整个游戏行为异常。
  - `AGENTS.md` / `README.md` —— 文档类文件，避免 AI 覆盖人工维护的内容。
  - `tests/test_game.py` —— 基线测试代码，防止 AI 无意中破坏已有测试逻辑。
  - `.github/workflows/*.yml` —— CI 工作流配置，保证自动化流程不被随意更改。
- 项目**未设置**更细粒度的目录级沙盒（如限制 AI 访问 `__pycache__` 或临时文件），也**未使用** CODEOWNERS 强制关键文件人工审核。

### 改进方案（已实施 / 建议）

| 问题 | 已落地改进 | 后续建议 |
|------|-----------|----------|
| 无明确约束文件 | ✅ 已创建 `.aiignore` | — |
| 核心文件可被任意修改 | ✅ 已列入禁止名单 | 可进一步增加 `CODEOWNERS`，要求核心文件变更必须由组长审核 |
| 未区分 AI 与人工修改边界 | ⚠️ 暂未实施 | 可探索 GitHub Copilot 企业策略或 pre-commit hook 标记 AI 生成代码 |

### 证据

> 以下为：`.aiignore` 文件完整内容，已限制 AI 修改 `constants.py`、`AGENTS.md`、`tests/test_game.py` 及 workflows 目录。
>
> ![下载](C:\Users\谢依i\OneDrive\Desktop\下载.png)

---

## 审计阀门二：告知（Inform）

**目标**：AI 是否能获得足够上下文来理解代码结构与约束。

### 当前状态

- 项目根目录**存在** `AGENTS.md` 文件，内容符合 Anthropic 渐进式披露范式。
- `AGENTS.md` 包含以下关键信息模块：
  - **架构概述**：说明这是 Python 控制台迷宫游戏，模块化分离（主循环、地图、玩家、命令处理、常量）。
  - **目录结构**：列出 `main.py` / `map.py` / `player.py` / `command.py` / `constants.py` / `tests/` 及其职责。
  - **核心职责表格**：明确 `MazeMap`（地图渲染/位置/碰撞）、`Player`（背包/拾取）、`CommandHandler`（输入/移动/终点检测）、`constants`（避免硬编码）。
  - **编码规范**：类名 `PascalCase`，函数 `camelCase`，移动必须做边界+墙体检查，使用常量代替魔法值。
  - **禁止操作清单**：不直接修改 `map_grid`，不硬编码游戏符号，不把渲染逻辑混入命令处理，移动前必须做碰撞检测。
  - **数据流向（树形图）**：从 `main.py` 游戏循环 → `process_input()` → `handle_move()` → `is_wall()` / `update_position()` → 物品拾取 → 终点检测。
  - **关键函数参考表格**：列出 `handle_move`、`is_wall`、`update_position`、`add_to_inventory`、`process_input` 及其所在模块和描述。
  - **扩展示例**：如何新增物品类型（修改 `constants.py` → 更新 `Player.add_to_inventory()` → 在地图中放置）。
  - **测试命令**：`python -m unittest tests/test_game.py` 和 `pytest` 用法。
- 上述内容使得一个从未接触过该项目的 AI 编程助手，仅凭 `AGENTS.md` 就能理解项目结构并生成符合规范的代码。

### 改进方案（已实施 / 建议）

| 维度 | 已落地改进 | 后续建议 |
|------|-----------|----------|
| 基础文档 | ✅ 架构+目录+职责+规范+禁止清单 | — |
| 上下文深度 | ✅ 数据流向 + 函数参考表 + 扩展示例 | 可增加常见任务的代码片段（如“如何加一个新命令”） |
| AI 可读性 | ✅ 采用 Markdown 表格、代码块、树形图混合结构 | — |

### 证据

> `AGENTS.md` 中“数据流向”章节（树形图）和“关键函数参考表格”， AI 能获取完整上下文。
>
> ![image-20260429152448466](C:\Users\谢依i\AppData\Roaming\Typora\typora-user-images\image-20260429152448466.png)
>
> ![image-20260429152515090](C:\Users\谢依i\AppData\Roaming\Typora\typora-user-images\image-20260429152515090.png)

---

## 审计阀门三：验证（Verify）

**目标**：AI 生成的代码是否有自动化测试验证。

### 当前状态

- 项目已配置 **GitHub Actions** 持续集成，定义在 `.github/workflows/ci-maze-game.yml`。
- CI 触发条件：
  - `push` 到 `main` / `develop` 分支
  - `pull_request` 到 `main` / `develop` 分支
- CI 运行内容：
  - 使用 `ubuntu-latest` + Python 3.10
  - 执行 `python -m unittest tests/test_game.py`
- 现有测试文件 `tests/test_game.py` 包含 **5 个有效测试用例**：
  1. `test_player_cannot_move_into_wall` —— 撞墙逻辑
  2. `test_player_pick_item` —— 物品拾取
  3. `test_invalid_command` —— 无效命令不崩溃
  4. `test_move_to_boundary` —— 边界移动不越界（新增边界测试）
  5. `test_multiple_items_pickup` —— 连续操作不崩溃（新增稳定性测试）
- **main 分支保护规则**已要求 CI 必须通过才能合并 PR（与阀门四联动）。
- 最近一次 CI 运行结果为 **✅ 绿色通过**。

### 改进方案（已实施 / 建议）

| 问题 | 已落地改进 | 后续建议 |
|------|-----------|----------|
| 无自动化测试 | ✅ 配置 GitHub Actions 运行 unittest | — |
| 测试覆盖不完整 | ✅ 补充边界测试（`test_move_to_boundary`）和稳定性测试 | 可增加覆盖率工具（`pytest-cov`）并设定 ≥70% 门禁 |
| CI 与分支保护割裂 | ✅ 分支保护要求 CI 通过 | — |
| 无测试报告可视化 | ⚠️ 尚未配置 | 可集成 Codecov 或 GitHub 测试报告插件 |

### 证据

> 此处插入截图：GitHub Actions 页面显示最新一次工作流为绿色 ✅，工作流名称为 “Maze Game CI Test”。
>
> ![下载 (1)](C:\Users\谢依i\OneDrive\Desktop\下载 (1).png)

> 此处插入截图：`tests/test_game.py` 中新增的边界测试代码（`test_move_to_boundary` 和 `test_multiple_items_pickup`）。
>
> ![image-20260429152753594](C:\Users\谢依i\AppData\Roaming\Typora\typora-user-images\image-20260429152753594.png)

---

## 审计阀门四：纠正（Correct）

**目标**：出错时能否一键回滚。

### 当前状态

- **main 分支已配置保护规则**：
  - `Require pull request before merging` —— 禁止直接 push
  - `Require approvals`（至少 1 人） —— 需要审核
  - `Dismiss stale pull request approvals` —— 代码更新后审核失效
  - `Require status checks to pass before merging` —— 绑定 `Maze Game CI Test`
  - `Block force pushes` —— 阻止 `git push -f` 覆盖历史
  - `Include administrators` —— 规则对管理员同样生效
- **回滚能力现状**：
  - 由于强制 PR + 审核 + CI，错误的 AI 生成代码**无法直接进入 main 分支**。
  - 一旦错误代码被合并（概率极低），可执行 `git revert <commit-hash>` 并走 PR 流程回滚。
  - **没有**一键回滚脚本或自动化 revert 工具，回滚需要手动操作。

### 改进方案（已实施 / 建议）

| 问题 | 已落地改进 | 后续建议 |
|------|-----------|----------|
| 可直接 push main | ✅ 禁止直接 push，强制 PR | — |
| 无审核门槛 | ✅ 要求 1 人 approve | 可根据团队规模调整为 2 人 |
| CI 不通过也可合并 | ✅ 要求 status check 通过 | — |
| 回滚依赖人工操作 | ⚠️ 目前无自动化 | 可编写 `rollback.sh` 脚本：`git revert` + `git push` + 自动创建回滚 PR |
| 无回滚演练 | ⚠️ 未进行 | 建议每月演练一次回滚流程 |

### 证据

> 此处插入截图：GitHub 分支保护规则配置页面，显示 main 分支已开启 `Require pull request`、`Require approvals`、`Require status checks`。
>
> ![image-20260429153509355](C:\Users\谢依i\AppData\Roaming\Typora\typora-user-images\image-20260429153509355.png)
>
> ![image-20260429153723121](C:\Users\谢依i\AppData\Roaming\Typora\typora-user-images\image-20260429153723121.png)
>
> ![image-20260429153559949](C:\Users\谢依i\AppData\Roaming\Typora\typora-user-images\image-20260429153559949.png)

> 此处插入截图：测试 PR 页面，显示 “At least 1 approving review is required” + “Merging is blocked” + “Merge pull request” 按钮灰色。
>
> ![下载 (2)](C:\Users\谢依i\OneDrive\Desktop\下载 (2).png)

---

## 综合结论

| 阀门 | 改进前风险 | 改进后状态 | 关键证据 |
|------|-----------|------------|----------|
| 约束（Constraint） | 无任何限制，AI 可改所有文件 | ✅ 已通过 `.aiignore` 限制 | `.aiignore` 截图 |
| 告知（Inform） | 上下文不足，AI 难以理解项目 | ✅ `AGENTS.md` 含数据流向+表格+示例 | `AGENTS.md` 数据流向截图 |
| 验证（Verify） | 无自动化测试 | ✅ GitHub Actions 自动运行 unittest，CI 绿色 | CI 绿色截图 + 测试代码截图 |
| 纠正（Correct） | 任何人都能直接 push main | ✅ 分支保护 + 强制 PR + 1人审核 + CI 必须通过 | 分支保护配置截图 + PR 灰色按钮截图 |

**整体评价**：本项目在 CIVC 四阀门上均已落地可验证的改进方案，薄弱环节（约束、验证、纠正）已从“无”提升到“工程可用”级别。`AGENTS.md` 满足渐进式披露范式，可让陌生 AI 高效理解项目。自动化测试与分支保护联动，阻止未验证代码合入主分支。回滚机制依赖 `git revert` 与 PR 流程，已具备基础可恢复能力。

---

## 改进落地总结

1. **约束阀门**：新增 `.aiignore`，明确禁止 AI 修改核心配置、文档、测试基线、CI 脚本。
2. **告知阀门**：重构 `AGENTS.md`，补充数据流向树形图、函数参考表、扩展示例，确保 AI 可独立理解项目。
3. **验证阀门**：配置 GitHub Actions，每次提交自动运行 unittest，并与分支保护规则联动。
4. **纠正阀门**：设置 main 分支保护（PR + 1人审核 + CI 通过 + 禁止 force push），阻止错误代码直接合入。

以上所有改动均已提交至仓库 main 分支，可在 Git 历史中追溯。

---

## 附录：证据清单

- [x] 截图 A：`.aiignore` 文件内容
- [x] 截图 B：`AGENTS.md` 数据流向章节 + 函数参考表格
- [x] 截图 C：GitHub Actions 页面绿色 ✅ 运行记录
- [x] 截图 D：`tests/test_game.py` 中新增的边界测试代码
- [x] 截图 E：main 分支保护规则配置页面
- [x] 截图 F：测试 PR 页面显示灰色 Merge 按钮 + “At least 1 approving review is required”

