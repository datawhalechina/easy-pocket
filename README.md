<div align="center">

```text
███████╗ █████╗ ███████╗██╗   ██╗    ██████╗  ██████╗  ██████╗██╗  ██╗███████╗████████╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝
█████╗  ███████║███████╗ ╚████╔╝     ██████╔╝██║   ██║██║     █████╔╝ █████╗     ██║   
██╔══╝  ██╔══██║╚════██║  ╚██╔╝      ██╔═══╝ ██║   ██║██║     ██╔═██╗ ██╔══╝     ██║   
███████╗██║  ██║███████╗   ██║       ██║     ╚██████╔╝╚██████╗██║  ██╗███████╗   ██║   
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝
```

# Easy-Pocket : 从零掌握 PocketFlow（⚠️ Alpha内测版）

> [!CAUTION]
> ⚠️ Alpha内测版本警告：此为早期内部构建版本，尚不完整且可能存在错误，欢迎大家提Issue反馈问题或建议。

<p align="center">
  <a href="https://github.com/The-Pocket/PocketFlow">PocketFlow 官方仓库</a> ·
  <a href="#内容导航">内容导航</a> ·
  <a href="#如何学习">如何学习</a>
</p>

<p align="center">
    <a href="https://github.com/zhimin-z/easy-pocket/stargazers" target="_blank">
        <img src="https://img.shields.io/github/stars/zhimin-z/easy-pocket?color=660874&style=for-the-badge&logo=star&logoColor=white&labelColor=1a1a2e" alt="Stars"></a>
    <a href="https://github.com/zhimin-z/easy-pocket/network/members" target="_blank">
        <img src="https://img.shields.io/github/forks/zhimin-z/easy-pocket?color=660874&style=for-the-badge&logo=git-fork&logoColor=white&labelColor=1a1a2e" alt="Forks"></a>
    <a href="LICENSE" target="_blank">
        <img src="https://img.shields.io/badge/License-CC_BY_NC_SA_4.0-4ecdc4?style=for-the-badge&logo=creative-commons&logoColor=white&labelColor=1a1a2e" alt="License"></a>
</p>

</div>

> **100 行代码，零依赖，构建 LLM 应用的一切。**

[PocketFlow](https://github.com/The-Pocket/PocketFlow) 是一个仅 100 行 Python 代码的极简 LLM 应用框架。它用 **Node**（节点）和 **Flow**（流程）两个核心抽象，让你可以构建聊天机器人、RAG、Agent、工作流等所有主流 LLM 应用。

**Easy-Pocket** 是 PocketFlow 的**交互式中文教程**，通过可视化演示和实战案例，带你从零理解框架原理、掌握应用开发。

---

## 内容导航

本教程分为两大篇章，覆盖原理到实战：

### 原理篇：PocketFlow 核心解析

| 章节 | 关键内容 |
| :--- | :--- |
| [引言：为什么需要 LLM 框架](docs/zh-cn/pocketflow-intro/index.md) | 核心痛点与框架对比 |
| [核心抽象：Node 与 Flow](docs/zh-cn/pocketflow-intro/index.md) | 三阶段模型、图执行引擎、操作符重载 |
| [Shared 通信机制](docs/zh-cn/pocketflow-intro/index.md) | 节点间数据传递的设计哲学 |
| [源码解剖：100 行的全部秘密](docs/zh-cn/pocketflow-intro/index.md) | BaseNode、Node、Flow、BatchNode、AsyncNode |
| [六大设计模式](docs/zh-cn/pocketflow-intro/index.md) | 链式、分支、循环、嵌套、批量、并行 |
| [Agentic Coding 开发范式](docs/zh-cn/pocketflow-intro/index.md) | 人类设计架构，AI 写代码 |

### 案例篇：从入门到进阶

| 案例 | 模式 | 难度 |
| :--- | :--- | :--- |
| [聊天机器人](docs/zh-cn/pocketflow-cases/index.md) | 链式 + 循环 | ⭐ |
| [RAG 检索增强](docs/zh-cn/pocketflow-cases/index.md) | 链式 + BatchNode | ⭐ |
| [写作工作流](docs/zh-cn/pocketflow-cases/index.md) | 链式 | ⭐ |
| [搜索 Agent](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 条件分支 | ⭐⭐ |
| [多 Agent 协作](docs/zh-cn/pocketflow-cases/index.md) | 多 Agent + 循环 | ⭐⭐ |
| [Map-Reduce 批处理](docs/zh-cn/pocketflow-cases/index.md) | BatchNode | ⭐ |
| [并行处理 (8x 加速)](docs/zh-cn/pocketflow-cases/index.md) | AsyncParallelBatchNode | ⭐⭐ |
| [思维链推理](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 自检 | ⭐⭐⭐ |
| [MCP 工具集成](docs/zh-cn/pocketflow-cases/index.md) | Agent + 工具 | ⭐⭐⭐ |
| [智能体编程](docs/zh-cn/pocketflow-cases/index.md) | 完整项目模板 | ⭐⭐⭐ |

---

## 如何学习

根据你的背景选择学习路径：

- **零基础**：原理篇全篇 → 案例篇（聊天机器人 → 写作工作流 → RAG）
- **想做 Agent**：原理篇 → 案例篇（搜索 Agent → 多 Agent → MCP → 智能体编程）
- **关注性能**：原理篇（BatchNode / AsyncNode）→ 案例篇（Map-Reduce → 并行处理）

---

## 示例代码

每篇教程都附带**完整可运行**的 Python 示例，无需 API 密钥，开箱即用。

### 快速开始

```bash
# 1. 确认 Python 版本（需要 3.9+）
python --version

# 2. 创建虚拟环境
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. 安装依赖
pip install pocketflow
```

### 示例文件夹

| 教程 | 示例目录 | 内容 |
| :--- | :--- | :--- |
| 原理入门 | [`docs/zh-cn/pocketflow-intro/examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-intro/examples) | 10 个脚本：Node 生命周期、Flow 图执行、条件分支、批处理、异步并发等 |
| 应用案例 | [`docs/zh-cn/pocketflow-cases/examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-cases/examples) | 10 个案例：ChatBot、RAG、Agent、工作流、多 Agent、Map-Reduce、MCP 等 |

> 所有示例使用模拟 LLM 实现，聚焦框架核心概念。如需接入真实 API，参见各目录下的 README 说明。

---

## 本地预览文档

```bash
npm install
npm run dev
# 打开 http://localhost:5173/easy-pocket/
```

---

## 项目结构

```
easy-pocket/
├── docs/
│   ├── .vitepress/              # VitePress 配置
│   ├── public/                  # 静态资源
│   └── zh-cn/
│       ├── pocketflow-intro/    # 原理入门教程
│       │   ├── index.md
│       │   └── examples/        # 10 个配套示例脚本
│       └── pocketflow-cases/    # 应用案例教程
│           ├── index.md
│           └── examples/        # 10 个配套案例脚本 + 项目模板
├── package.json
└── README.md
```

---

## 参与贡献

- 发现问题或有改进建议？欢迎 [提 Issue](https://github.com/zhimin-z/easy-pocket/issues)
- 想参与内容贡献？欢迎 [提 Pull Request](https://github.com/zhimin-z/easy-pocket/pulls)

---

## LICENSE

<div align="center">
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
  <img
    alt="知识共享许可协议"
    style="border-width:0"
    src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey"
  />
</a>
<br />
本作品采用
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
  知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议
</a>
进行许可。
</div>
