---
title: '核心抽象：Node 与 Flow'
description: 'PocketFlow 的两个核心概念：Node 三阶段执行模型与 Flow 图编排引擎。'
---

# 2. 核心抽象：只有两个概念

PocketFlow 的全部设计可以用一句话概括：

> **Node**（节点）负责"做事"，**Flow**（流程）负责"调度"。

就这两个概念，没有更多了。

### 2.1 Node —— 执行的最小单元

每个 Node 都遵循**三阶段执行模型**：

| `prep(shared)` | → | `exec(prep_res)` | → | `post(shared, prep_res, exec_res)` |
|:---:|:---:|:---:|:---:|:---:|
| 准备数据 | → | 执行逻辑 | → | 后处理 & 决策 |

- **prep**：从共享存储 `shared` 中**读取**所需数据
- **exec**：执行核心业务逻辑（如调用 LLM API）
- **post**：将结果**写回** `shared`，并返回一个 `action` 字符串

<div align="center"><img src="/node.png" width="380"/></div>

*Node：单步推理的最小执行单元*

<NodeLifecycleDemo />

::: tip 为什么要分三个阶段？
分三阶段的好处在于**解耦**：
- `prep` 和 `post` 负责和外部世界（shared）交互
- `exec` 是纯粹的业务逻辑，完全不知道 shared 的存在
- 这让 `exec` 可以被独立测试、独立重试、独立替换
:::

::: warning node.run() vs flow.run()
直接调用 `node.run(shared)` 只会执行**这一个节点**，不会沿着 `>>` 连接运行后继节点。如果你连接了后继，PocketFlow 会发出警告：*"Node won't run successors. Use Flow."* 要让整条链路跑起来，必须用 `Flow(start=node).run(shared)`。
:::

### 2.2 Flow —— 图编排引擎

Flow 做的事情非常简单：

1. 从 `start_node` 开始
2. 执行当前节点的 `_run(shared)`
3. 根据返回的 `action` 找到下一个节点
4. 重复，直到没有后继节点

```python
# Flow 的核心循环（伪代码）
curr = start_node
while curr:
    action = curr._run(shared)       # 执行节点
    curr = curr.successors[action]    # 跳转到下一个
```

<div align="center"><img src="/flow.png" width="380"/></div>

*Flow：串联多个 Node，实现多步推理*

<FlowGraphDemo />

### 2.3 连接节点的两种方式

PocketFlow 通过 Python 操作符重载，让节点连接变得极其优雅：

```python
# 方式 1：默认连接（>> 操作符）
node_a >> node_b >> node_c
# 等价于：node_a.next(node_b, "default")

# 方式 2：条件连接（- 操作符）
check_node - "approve" >> approve_node
check_node - "reject"  >> reject_node
# 等价于：check_node.next(approve_node, "approve")
```

<div align="center"><img src="/branch.png" width="380"/></div>

*条件分支：根据 action 字符串走不同路径*

::: info 这里发生了什么？
- `>>` 重载了 `__rshift__` 方法，调用 `self.next(other, "default")`
- `-` 重载了 `__sub__` 方法，返回一个 `_ConditionalTransition` 对象
- `_ConditionalTransition` 的 `>>` 再调用 `src.next(tgt, action)`
- 两层操作符重载，实现了直观的图构建语法
:::

### 2.4 形式化视角：PocketFlow 即有限状态自动机

:::: details 可选阅读 —— 本节从理论角度解析 PocketFlow，不影响后续学习。如果你只想快速上手，可以跳过直接进入 [§3 通信机制](./communication-and-patterns#_3-通信机制-shared-store-与-params)。

如果你学过编译原理或形式语言，会发现 PocketFlow 的执行模型和**有限状态自动机**（Finite State Automaton, FSA）几乎同构。这不是巧合 —— PocketFlow 的设计就是在 LLM 场景下实现了一台 FSA。

#### 五元组映射

一台 FSA 由五元组 (Q, Σ, δ, q₀, F) 定义，它们和 PocketFlow 的对应关系如下：

| FSA 形式定义 | PocketFlow 对应 | 示例 |
| :--- | :--- | :--- |
| **状态集 Q** | 所有 Node 实例 | `{think, search, synthesize}` |
| **字母表 Σ** | Action 字符串的集合 | `{"need_more", "enough", "default"}` |
| **转移函数 δ(q, a)** | `node - "action" >> next_node` 建立的后继映射 | `think - "need_more" >> search` |
| **初始状态 q₀** | `Flow(start=node)` 的起始节点 | `Flow(start=think)` |
| **终止条件** | `post()` 返回的 action 在后继映射中找不到 → 流程结束 | `post()` 返回 `None` |

#### 应用模式 = 自动机拓扑

不同 LLM 应用模式，实际上对应不同形态的自动机。下面是三个典型例子：

**1. 聊天机器人** —— 单状态 + 自环，最简单的循环结构

> ChatNode 的 `post()` 返回 `"continue"` 时跳回自身，形成对话循环；返回 `None` 时无后继节点，Flow 结束。

**2. 搜索智能体** —— 分支 + 环，LLM 决定转移方向

> Think 通过 `"need_more"` 跳转 Search；Search 完成后 `"default"` 回到 Think 继续判断；Think 认为信息足够时 `"enough"` 进入 Synthesize 输出结果。

**3. 结构化输出** —— 回退边，校验失败回退重试

> Generate 生成 → Validate 校验 → Check 判断：校验不通过时 `"retry"` 回到 Generate 重新生成；校验通过时 `"done"` 进入 Output 输出结果。

更多模式一览：

| 应用模式 | 自动机形态 | 状态数 | 特征 |
| :--- | :--- | :--- | :--- |
| 聊天机器人 | 单状态 + 自环 | 1 | 最简单的循环 |
| 写作工作流 | 线性链 | 3 | 无分支、无环 |
| 搜索智能体 | 分支 + 环 | 3 | LLM 决定转移方向 |
| 结构化输出 | 回退边 | 3-4 | 校验失败回退重试 |
| 多智能体 | 并发自动机组 | N×M | 多台自动机通过队列通信 |

::: tip 与 LangGraph"状态机"的区别
LangGraph 也自称"状态机"，但含义不同：
- **LangGraph 的"状态"** = 运行时数据（TypedDict），框架管理状态的持久化、快照和回放
- **PocketFlow 的"状态"** = 当前所在的 Node，数据由你自己在 `shared` 中管理

PocketFlow 更接近经典 FSA：**状态转移由 action 字符串驱动，状态数据在自动机之外管理**。这让框架保持在 100 行，同时你可以自由选择任何持久化方案。
:::
::::
