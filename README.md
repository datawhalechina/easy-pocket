<div align="center">

<img width="2752" height="1536" alt="Easy-Pocket 核心概念宣传图_高清紧凑版" src="https://github.com/user-attachments/assets/e056fbcc-bf62-4ab9-b2ea-00d51720abca" />

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

[PocketFlow](https://github.com/The-Pocket/PocketFlow) 是一个仅 100 行 Python 代码的极简 LLM 应用框架。它用 **Node**（节点）和 **Flow**（流程）两个核心抽象，让你可以构建聊天机器人、RAG、智能体、工作流等所有主流 LLM 应用。

**Easy-Pocket** 是 PocketFlow 的**交互式中文教程**，通过可视化演示和实战案例，带你从零理解框架原理、掌握应用开发。

---

## PocketFlow 是什么？

PocketFlow 是一个**纯编排框架**（Orchestration Framework）—— 它只负责**调度节点、管理流程、传递数据**，不包含任何 LLM 调用、Embedding 计算或向量存储的实现。

```text
┌───────────────────────────────────────────────────────┐
│  你的应用                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
│  │  Node A  │──>│  Node B  │──>│  Node C  │           │
│  │ (调LLM)  │   │ (查向量库)│   │ (写数据库)│           │
│  └──────────┘   └──────────┘   └──────────┘           │
│        │              │              │                │
│  ┌─────┴──────────────┴──────────────┴────┐           │
│  │       PocketFlow 编排层                 │ <-- 100行 │
│  │ Node 生命周期 · Flow 图遍历 · 数据传递   │           │
│  └─────┬──────────────┬──────────────┬────┘           │
│        │              │              │                │
│  ┌─────┴────┐   ┌─────┴────┐   ┌─────┴────┐           │
│  │  OpenAI  │   │ Pinecone │   │ Postgres │ <-- 你选  │
│  │  Claude  │   │  FAISS   │   │  Redis   │           │
│  │ 本地模型  │   │  Chroma  │   │   ...    │           │
│  └──────────┘   └──────────┘   └──────────┘           │
└───────────────────────────────────────────────────────┘
```

| | PocketFlow 负责 | 你来决定 |
| :--- | :--- | :--- |
| **LLM** | 节点何时被调用、按什么顺序 | 用哪家 API（OpenAI / Claude / 本地模型） |
| **Embedding** | 批量处理的并行调度 | 用哪个模型和向量数据库 |
| **Memory** | shared 字典的读写传递 | 怎么持久化（文件 / Redis / 数据库） |
| **工具调用** | 智能体 循环的执行与分支 | 调用哪些外部 API 和工具 |

> **一句话定位**：PocketFlow = 图的运行时。你把具体实现填进 Node 的 `exec()` 方法，PocketFlow 负责把它们串成流程。

如果你学过编译原理或形式语言，会发现 PocketFlow 的执行模型就是一台**有限状态自动机**（Finite State Automaton）：

| FSA 形式定义 | PocketFlow 对应 |
| :--- | :--- |
| 状态集 Q | Node 集合 |
| 字母表 Σ | Action 字符串集（`"continue"`、`"retry"`、`"done"` …） |
| 转移函数 δ(q, a) | `node - "action" >> next_node` |
| 初始状态 q₀ | `Flow(start=node)` |
| 终止 | `post()` 返回的 action 无后继节点 → 流程结束 |

不同 LLM 应用模式，对应不同的自动机拓扑：聊天机器人是带自环的单状态机，智能体 是有分支+环的自动机，结构化输出是带回退边的自动机。详见[原理篇 §2.4](docs/zh-cn/pocketflow-intro/index.md)。

---

## 与其他编排框架的对比

理解了 PocketFlow 的定位后，我们可以将它与同一层级的编排框架进行对比。这些框架都解决"如何组织 LLM 调用"的问题，但设计哲学截然不同：

> 其他框架给你**预制组件**（智能体 类、RAG 管道、Memory 模块），你在框架规定的结构里填写逻辑。
>
> PocketFlow 给你**图论原语**（Node + Flow），你用这两块积木**自己搭建**一切。

| 框架 | 核心思路 | 代码量 | 依赖 | 厂商锁定 |
| :--- | :--- | :--- | :--- | :--- |
| **PocketFlow** | 最小有向图运行时：Node + Flow | **100 行** | **0** | **无** |
| Agno | 声明式 智能体，内置 Memory / Knowledge | 数千行 | 少 | 低 |
| AutoGen | Actor 模型，智能体 间异步消息传递 | 数万行 | 中 | 低-中 |
| CrewAI | 角色扮演团队，Manager 分配 Task | 数万行 | 中 | 低 |
| LangGraph | 有状态状态机 + 持久化检查点 | 数万行 | 多（LangChain 生态） | 中 |
| OpenAI Agents SDK | 轻量 智能体 + Handoff + Guardrails | 数千行 | 少 | 中（OpenAI 优先） |
| PydanticAI | 类型安全的函数调用 + Pydantic 验证 | 数千行 | 少 | 很低 |
| SmolAgents | LLM 生成 Python 代码而非 JSON tool call | ~1000 行 | 少 | 很低 |

PocketFlow 没有 `AgentExecutor`、`RetrievalChain`、`CrewManager` 这样的专用类 —— 所有模式都是同一套 Node + Flow 的不同图拓扑（见上方 [FSA 映射](#pocketflow-是什么)）。

---

## 内容导航

本教程分为两大篇章，覆盖原理到实战：

### 原理篇：PocketFlow 核心解析

| 章节 | 关键内容 |
| :--- | :--- |
| [引言：为什么需要 LLM 框架](docs/zh-cn/pocketflow-intro/index.md) | 核心痛点与框架对比 |
| [核心抽象：Node 与 Flow](docs/zh-cn/pocketflow-intro/index.md) | 三阶段模型、图执行引擎、操作符重载、FSA 形式化视角 |
| [通信机制：Shared 与 Params](docs/zh-cn/pocketflow-intro/index.md) | Shared Store 全局共享 + Params 局部参数 |
| [六大设计模式](docs/zh-cn/pocketflow-intro/index.md) | 链式、分支、循环、嵌套、批量、并行 |
| [源码解剖：100 行的全部秘密](docs/zh-cn/pocketflow-intro/index.md) | BaseNode、Node、Flow、BatchNode、BatchFlow、AsyncNode |
| [工具函数层：Node 里装什么？](docs/zh-cn/pocketflow-intro/index.md) | LLM 调用、Web 搜索、Embedding、向量数据库等工具函数分类 |
| [Agentic Coding 开发范式](docs/zh-cn/pocketflow-intro/index.md) | 人类设计架构，AI 写代码 |

### 案例篇：从入门到进阶

| # | 案例 | 模式 | 难度 |
| :--- | :--- | :--- | :--- |
| 1 | [聊天机器人](docs/zh-cn/pocketflow-cases/index.md) | 链式 + 循环 | ⭐ |
| 2 | [写作工作流](docs/zh-cn/pocketflow-cases/index.md) | 链式 | ⭐ |
| 3 | [RAG 检索增强](docs/zh-cn/pocketflow-cases/index.md) | 链式 + BatchNode | ⭐ |
| 4 | [搜索智能体](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 条件分支 | ⭐⭐ |
| 5 | [多智能体 协作](docs/zh-cn/pocketflow-cases/index.md) | AsyncNode + 消息队列 | ⭐⭐ |
| 6 | [Map-Reduce 批处理](docs/zh-cn/pocketflow-cases/index.md) | BatchNode | ⭐ |
| 7 | [并行处理 (8x 加速)](docs/zh-cn/pocketflow-cases/index.md) | AsyncParallelBatchNode | ⭐⭐ |
| 8 | [结构化输出](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 重试 + 校验 | ⭐⭐ |
| 9 | [思维链推理](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 自检 | ⭐⭐⭐ |
| 10 | [MCP 工具集成](docs/zh-cn/pocketflow-cases/index.md) | 智能体 + 工具 | ⭐⭐⭐ |
| 11 | [智能体编程](docs/zh-cn/pocketflow-cases/index.md) | 完整项目模板 | ⭐⭐⭐ |
| 12 | [智能体技能](docs/zh-cn/pocketflow-cases/index.md) | 链式 + 条件路由 | ⭐⭐ |

---

## 如何学习

根据你的背景选择学习路径：

- **零基础**：原理篇全篇 → 案例篇（聊天机器人 → 写作工作流 → RAG）
- **想做 智能体**：原理篇 → 案例篇（搜索智能体 → 多智能体 → 智能体技能 → MCP → 智能体编程）
- **关注性能**：原理篇（BatchNode / AsyncNode）→ 案例篇（Map-Reduce → 并行处理）
- **输出质量**：原理篇（循环/重试）→ 案例篇（结构化输出 → 思维链推理）

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
| 应用案例 | [`docs/zh-cn/pocketflow-cases/examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-cases/examples) | 12 个案例：ChatBot、写作工作流、RAG、智能体、多智能体、Map-Reduce、结构化输出、MCP、智能体技能 等 |

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
│           └── examples/        # 12 个配套案例脚本 + 项目模板
├── package.json
└── README.md
```

---

## 参与贡献

- 发现问题或有改进建议？欢迎 [提 Issue](https://github.com/zhimin-z/easy-pocket/issues)
- 想参与内容贡献？欢迎 [提 Pull Request](https://github.com/zhimin-z/easy-pocket/pulls)

---

## LICENSE

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
