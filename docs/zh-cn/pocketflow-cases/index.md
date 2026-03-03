---
title: 'PocketFlow 应用案例 —— 从入门到进阶的实战全景'
description: '通过 12 个实战案例，学习如何用 PocketFlow 构建聊天机器人、RAG、智能体、工作流、批处理等 LLM 应用。'
---

# PocketFlow 应用案例（Application Cases）

> **学习指南**：本章精选了 PocketFlow 的 12 个应用案例，从入门到进阶，覆盖聊天、RAG、智能体、批处理、并行等常见模式。每个案例都包含 Flow 架构图、核心代码和学习要点。

<CaseShowcase />


## 0. 案例地图：选择你的学习路径

不同背景的读者可以选择不同的入门路径：

<el-tabs type="border-card">
  <el-tab-pane label="零基础入门">

**推荐顺序**：[聊天机器人](./beginner#_1-聊天机器人-chatbot) → [写作工作流](./beginner#_2-写作工作流-writing-workflow) → [RAG](./beginner#_3-rag-检索增强生成)

这三个案例覆盖了 PocketFlow 的核心模式：链式调用、循环、条件分支、BatchNode。掌握它们，你就能构建大多数 LLM 应用。

  </el-tab-pane>
  <el-tab-pane label="想做智能体">

**推荐顺序**：[搜索智能体](./agents#_4-搜索智能体) → [多智能体协作](./agents#_5-多智能体协作) → [智能体技能](./advanced-agents#_11-智能体技能-技能路由) → [MCP 工具集成](./advanced-agents#_10-mcp-工具集成) → [智能体编程](./agentic-coding#_12-智能体编程-agentic-coding)

智能体 的核心是"自主决策循环"。这五个案例从简单的工具调用，到多智能体协作，再到技能路由和标准化工具集成，最后学习系统化构建 智能体 的工程方法论。

  </el-tab-pane>
  <el-tab-pane label="关注性能">

**推荐顺序**：[Map-Reduce 批处理](./batch-and-parallel#_6-map-reduce-批处理) → [并行处理](./batch-and-parallel#_7-并行处理-8x-加速)

BatchNode 和 AsyncParallelBatchNode 是 PocketFlow 处理性能问题的核心工具。这两个案例展示如何用简洁的代码获得数倍加速。

  </el-tab-pane>
  <el-tab-pane label="输出质量">

**推荐顺序**：[结构化输出](./output-quality#_8-结构化输出-structured-output) → [思维链推理](./output-quality#_9-思维链推理-chain-of-thought)

这两个案例展示如何提升 LLM 输出的可靠性：结构化输出确保格式正确可解析，思维链推理提升逻辑推理的准确性。

  </el-tab-pane>
</el-tabs>
