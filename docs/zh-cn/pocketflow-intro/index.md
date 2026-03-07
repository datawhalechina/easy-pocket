---
title: 'PocketFlow 原理入门 —— 100 行代码的极简 LLM 框架'
description: '从零理解 PocketFlow 的核心原理：Node 三阶段模型、Flow 图编排、Shared 与 Params 通信、Batch 批处理与 Async 异步并发。'
---

# PocketFlow 原理入门（Interactive Intro to PocketFlow）

> **学习指南**：本章节只需要基础的 Python 知识，通过交互式演示带你了解 PocketFlow —— 一个仅 100 行代码、零依赖的 LLM 应用框架。从"它能做什么"讲起，一直到"它是怎么做到的"。
>
> **多语言版本**：[Python](https://github.com/The-Pocket/PocketFlow) · [TypeScript](https://github.com/The-Pocket/PocketFlow-Typescript) · [Java](https://github.com/The-Pocket/PocketFlow-Java) · [C++](https://github.com/The-Pocket/PocketFlow-CPP) · [Go](https://github.com/The-Pocket/PocketFlow-Go) · [Rust](https://github.com/The-Pocket/PocketFlow-Rust) · [PHP](https://github.com/The-Pocket/PocketFlow-PHP)

<PocketFlowQuickStart />


## 0. 引言：为什么需要 LLM 框架？

大语言模型（LLM）本身只是一个"文字接龙"引擎 —— 你给它一段文字，它预测下一个词。

但要把 LLM 变成**真正有用的应用**，你需要解决三个核心问题：

1. **流程编排**：如何把多个步骤（检索、生成、验证）串联成完整的流程？
2. **状态管理**：步骤之间如何传递数据？对话历史怎么管理？
3. **容错与扩展**：API 调用失败了怎么办？如何批量处理大量数据？

市面上的框架（LangChain、CrewAI 等）用**数万到数十万行代码**来解决这些问题。

而 PocketFlow 的回答是：**100 行就够了。**

<FrameworkCompareDemo />

### 0.1 框架全景：PocketFlow 与主流框架的本质区别

:::: details 初次阅读可跳过 —— 先跑通代码，再回来对比框架差异

在深入学习之前，先建立一个关键认知 —— PocketFlow 和其他框架**不在同一个抽象层级**：

| 框架 | 核心心智模型 | 给你的是什么 |
| :--- | :--- | :--- |
| **[Agno](https://github.com/agno-agi/agno)** | 声明式记忆代理 | 智能体 构造器内置 Memory + Knowledge + Tools |
| **[AutoGen](https://github.com/microsoft/autogen)** | Actor 消息传递 | 智能体 是 Actor，通过异步消息协作 |
| **[CrewAI](https://github.com/crewAIInc/crewAI)** | 角色扮演团队 | 智能体（角色/目标/背景故事）+ Manager 分配 Task |
| **[LangGraph](https://github.com/langchain-ai/langgraph)** | 有状态状态机 | 强类型 State + 条件边函数 + 持久化检查点 |
| **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** | 轻量 智能体 + Handoff | 智能体 + Handoff + Guardrails + Tracing |
| **[PydanticAI](https://github.com/pydantic/pydantic-ai)** | 类型安全函数 | 智能体 = 带 Pydantic 验证的函数调用 |
| **[SmolAgents](https://github.com/huggingface/smolagents)** | 代码即动作 | LLM 直接生成 Python 代码而非 JSON tool call |
| **[PocketFlow](https://github.com/The-Pocket/PocketFlow)** | **最小有向图运行时** | **只有 Node + Flow 两个原语，其他一切自己搭** |

::: tip 类比理解
可以把这些框架想象成不同的建筑方式：

- **LangGraph / CrewAI / AutoGen** = **精装房** —— 框架替你预制了"智能体 客厅"、"RAG 厨房"、"Memory 卧室"，你在现有房间里摆家具
- **PydanticAI / Agno / SmolAgents** = **毛坯房** —— 给你墙体和水电，你自己做装修
- **PocketFlow** = **一块地 + 物理定律** —— 只给你"节点"和"连线"这两条规则，你从地基开始搭

PocketFlow 的 100 行代码相当于"物理定律" —— **少到不能再少，但足以构建一切。**
:::

这意味着 PocketFlow 里**没有任何预制模式类** —— RAG、智能体、CoT、MapReduce 都是你用 Node + Flow 搭出来的不同图拓扑。

> **"Every LLM application is a directed graph. Nothing more."**
> —— PocketFlow 创作者 Zachary Huang

理解了这一点，接下来学习 Node 和 Flow 时你会发现：它们不是"框架的功能"，而是"图的物理定律"。具体的图拓扑与自动机映射，见 [§2.4 形式化视角](./core-abstractions#_2-4-形式化视角-pocketflow-即有限状态自动机)。
::::

### 0.2 PocketFlow 架构总览

::: details 初次阅读可跳过 —— 先跑通代码，学完再回来看全貌

PocketFlow 的 100 行源码由 **12 个类**组成，分为两大家族，通过三种机制通信：

<div align="center"><img src="/pocketflow-architecture.png" width="520"/></div>

*PocketFlow 架构：Node 家族（执行）+ Flow 家族（调度）+ 三种通信机制*

| 维度 | 同步 | 异步顺序 | 异步并行 |
| :--- | :--- | :--- | :--- |
| **单节点** | `Node` | `AsyncNode` | — |
| **批量节点** | `BatchNode` | `AsyncBatchNode` | `AsyncParallelBatchNode` |
| **流程** | `Flow` | `AsyncFlow` | — |
| **批量流程** | `BatchFlow` | `AsyncBatchFlow` | `AsyncParallelBatchFlow` |

> 12 个类 = BaseNode 基类 + 上表 10 个组合 + `_ConditionalTransition` 辅助类。详细继承关系见 [§5 深入源码](./source-code#_5-深入源码-100-行的全部秘密)。
:::
