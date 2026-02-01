<div align="center">

<pre style="font-family: 'Courier New', monospace; font-size: 16px; color: #000000; margin: 0; padding: 0; line-height: 1.2; transform: skew(-1deg, 0deg); display: block;">
███████╗ █████╗ ███████╗██╗   ██╗    ██████╗  ██████╗  ██████╗██╗  ██╗███████╗████████╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝
█████╗  ███████║███████╗ ╚████╔╝     ██████╔╝██║   ██║██║     █████╔╝ █████╗     ██║
██╔══╝  ██╔══██║╚════██║  ╚██╔╝      ██╔═══╝ ██║   ██║██║     ██╔═██╗ ██╔══╝     ██║
███████╗██║  ██║███████║   ██║       ██║     ╚██████╔╝╚██████╗██║  ██╗███████╗   ██║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   
</pre>

# Easy-Pocket : 从零掌握 PocketFlow

<p align="center">
  <a href="https://github.com/The-Pocket/PocketFlow">PocketFlow 官方仓库</a> ·
  <a href="#内容导航">内容导航</a> ·
  <a href="#如何学习">如何学习</a>
</p>

<p align="center">
    <a href="https://github.com/zhimi/easy-pocket/stargazers" target="_blank">
        <img src="https://img.shields.io/github/stars/zhimi/easy-pocket?color=660874&style=for-the-badge&logo=star&logoColor=white&labelColor=1a1a2e" alt="Stars"></a>
    <a href="https://github.com/zhimi/easy-pocket/network/members" target="_blank">
        <img src="https://img.shields.io/github/forks/zhimi/easy-pocket?color=660874&style=for-the-badge&logo=git-fork&logoColor=white&labelColor=1a1a2e" alt="Forks"></a>
    <a href="LICENSE" target="_blank">
        <img src="https://img.shields.io/badge/License-CC_BY_NC_SA_4.0-4ecdc4?style=for-the-badge&logo=creative-commons&logoColor=white&labelColor=1a1a2e" alt="License"></a>
</p>

</div>

> **100 行代码，零依赖，构建 LLM 应用的一切。**

[PocketFlow](https://github.com/The-Pocket/PocketFlow) 是一个仅 100 行 Python 代码的极简 LLM 应用框架。它用 **Node**（节点）和 **Flow**（流程）两个核心抽象，让你可以构建聊天机器人、RAG、Agent、工作流等所有主流 LLM 应用。

**Easy-Pocket** 是 PocketFlow 的**交互式中文教程**，通过可视化演示和实战案例，带你从零理解框架原理、掌握应用开发。

---

## 亮点

| 特性 | 说明 |
| :--- | :--- |
| **源码级讲解** | 逐类解剖 100 行核心代码：BaseNode → Node → Flow → BatchNode → AsyncNode |
| **交互式演示** | 每个概念配有可视化组件，在动手实验中理解 Node 生命周期、Flow 图执行 |
| **9 大案例** | 聊天机器人、RAG、Agent、写作工作流、多 Agent、批处理、并行处理等 |
| **框架对比** | 与 LangChain、CrewAI、AutoGen 的全维度对比，理解极简设计的价值 |
| **Agentic Coding** | 人类设计架构 + AI 写实现代码的新范式 |

---

## 内容导航

本教程分为两大篇章，覆盖原理到实战：

### 原理篇：PocketFlow 核心解析

| 章节 | 关键内容 | 状态 |
| :--- | :--- | :--- |
| [引言：为什么需要 LLM 框架](docs/zh-cn/pocketflow-intro/index.md) | 核心痛点与框架对比 | ✅ |
| [核心抽象：Node 与 Flow](docs/zh-cn/pocketflow-intro/index.md) | 三阶段模型、图执行引擎、操作符重载 | ✅ |
| [Shared 通信机制](docs/zh-cn/pocketflow-intro/index.md) | 节点间数据传递的设计哲学 | ✅ |
| [源码解剖：100 行的全部秘密](docs/zh-cn/pocketflow-intro/index.md) | BaseNode、Node、Flow、BatchNode、AsyncNode | ✅ |
| [六大设计模式](docs/zh-cn/pocketflow-intro/index.md) | 链式、分支、循环、嵌套、批量、并行 | ✅ |
| [Agentic Coding 开发范式](docs/zh-cn/pocketflow-intro/index.md) | 人类设计架构，AI 写代码 | ✅ |

### 案例篇：从入门到进阶

| 案例 | 模式 | 难度 | 状态 |
| :--- | :--- | :--- | :--- |
| [聊天机器人](docs/zh-cn/pocketflow-cases/index.md) | 链式 + 循环 | ⭐ | ✅ |
| [RAG 检索增强](docs/zh-cn/pocketflow-cases/index.md) | 链式 + BatchNode | ⭐ | ✅ |
| [写作工作流](docs/zh-cn/pocketflow-cases/index.md) | 链式 | ⭐ | ✅ |
| [搜索 Agent](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 条件分支 | ⭐⭐ | ✅ |
| [多 Agent 协作](docs/zh-cn/pocketflow-cases/index.md) | 多 Agent + 循环 | ⭐⭐ | ✅ |
| [Map-Reduce 批处理](docs/zh-cn/pocketflow-cases/index.md) | BatchNode | ⭐ | ✅ |
| [并行处理 (8x 加速)](docs/zh-cn/pocketflow-cases/index.md) | AsyncParallelBatchNode | ⭐⭐ | ✅ |
| [思维链推理](docs/zh-cn/pocketflow-cases/index.md) | 循环 + 自检 | ⭐⭐⭐ | ✅ |
| [MCP 工具集成](docs/zh-cn/pocketflow-cases/index.md) | Agent + 工具 | ⭐⭐⭐ | ✅ |

---

## 如何学习

根据你的背景选择学习路径：

- **零基础**：原理篇全篇 → 案例篇（聊天机器人 → 写作工作流 → RAG）
- **想做 Agent**：原理篇 → 案例篇（搜索 Agent → 多 Agent → MCP）
- **关注性能**：原理篇（BatchNode / AsyncNode）→ 案例篇（Map-Reduce → 并行处理）

---

## 本地启动

### 快捷方式

在 AI IDE（VS Code / Cursor / Trae）对话框中输入：

```
请帮我运行这个项目的本地服务
```

### 手动启动

```bash
npm install
npm run dev
# 打开 http://localhost:5173/easy-pocket/
```

---

## 参与贡献

- 发现问题或有改进建议？欢迎 [提 Issue](https://github.com/zhimi/easy-pocket/issues)
- 想参与内容贡献？欢迎 [提 Pull Request](https://github.com/zhimi/easy-pocket/pulls)

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
