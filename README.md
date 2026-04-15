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

## Sprint 3 工程基准实现
### 1. GitHub Actions自动化流水线
- 配置文件路径：`.github/workflows/ci.yml`
- 功能：PR提交至`develop`分支时，自动触发Python语法编译检查与单元测试，确保主干分支持续处于Green Build状态。
- 执行结果：流水线运行成功率100%，无失败构建记录。

### 2. OpenAPI接口契约归档
- 契约文件路径：`docs/api/contract.yaml`
- 功能：定义迷宫游戏用户登录、地图加载等核心业务接口，作为前后端Mock开发与集成联调的统一依据。

### 3. Git Flow分支治理
- 分支规范：所有功能开发基于`feature/*`分支进行，本次迭代创建`feature/ci-config`（CI配置）、`feature/update-report`（文档更新）分支。
- PR评审：已完成2次完整PR评审流程，所有代码合并前均通过两位评审人审核。

### 4. Mock环境闭环测试
- 工具：使用Prism挂载OpenAPI契约文件搭建Mock服务器。
- 成果：完成用户登录页、游戏地图页两个核心页面的逻辑闭环与边界测试，前端交互在后端接口未就绪时可正常运行。

---

## 关于我们

CodeWeavers是一支由AI赋能的敏捷开发小队，致力于用Scrum方法论和AI编程工具，将每一行代码编织成优雅的解决方案。
