---
title: 'PocketFlow 原理入门 —— 100 行代码的极简 LLM 框架'
description: '从零理解 PocketFlow 的核心原理：Node 三阶段模型、Flow 图编排、Shared 与 Params 通信、Batch 批处理与 Async 异步并发。'
---

# PocketFlow 原理入门 (Interactive Intro to PocketFlow)

> **学习指南**：本章节只需要基础的 Python 知识，通过交互式演示带你了解 PocketFlow —— 一个仅 100 行代码、零依赖的 LLM 应用框架。从"它能做什么"讲起，一直到"它是怎么做到的"。

<PocketFlowQuickStart />

---

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

::: details 💡 初次阅读可跳过 —— 先跑通代码，再回来对比框架差异
:::

在深入学习之前，先建立一个关键认知 —— PocketFlow 和其他框架**不在同一个抽象层级**：

| 框架 | 核心心智模型 | 给你的是什么 |
| :--- | :--- | :--- |
| **Agno** | 声明式记忆代理 | 智能体 构造器内置 Memory + Knowledge + Tools |
| **AutoGen** | Actor 消息传递 | 智能体 是 Actor，通过异步消息协作 |
| **CrewAI** | 角色扮演团队 | 智能体（角色/目标/背景故事）+ Manager 分配 Task |
| **LangGraph** | 有状态状态机 | 强类型 State + 条件边函数 + 持久化检查点 |
| **OpenAI Agents SDK** | 轻量 智能体 + Handoff | 智能体 + Handoff + Guardrails + Tracing |
| **PydanticAI** | 类型安全函数 | 智能体 = 带 Pydantic 验证的函数调用 |
| **SmolAgents** | 代码即动作 | LLM 直接生成 Python 代码而非 JSON tool call |
| **PocketFlow** | **最小有向图运行时** | **只有 Node + Flow 两个原语，其他一切自己搭** |

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

理解了这一点，接下来学习 Node 和 Flow 时你会发现：它们不是"框架的功能"，而是"图的物理定律"。具体的图拓扑与自动机映射，见 [§2.4 形式化视角](#_2-4-形式化视角-pocketflow-即有限状态自动机)。

---

## 1. 快速上手

先跑起来，再理解原理。

### 1.1 环境配置

#### Python 版本

PocketFlow 需要 **Python 3.9+**（推荐 3.10 或更高版本）：

```bash
python --version
```

#### 创建虚拟环境（推荐）

::: code-group

```bash [Windows]
python -m venv .venv
.venv\Scripts\activate
```

```bash [macOS / Linux]
python -m venv .venv
source .venv/bin/activate
```

:::

### 1.2 安装 PocketFlow

::: code-group

```bash [pip]
pip install pocketflow
```

```bash [指定版本]
# 如需锁定版本（教程编写时为 0.0.3）
pip install pocketflow==0.0.3
```

```bash [复制源码]
# PocketFlow 只有 100 行，也可以直接复制到项目中
# https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py
```

:::

::: tip 零依赖
PocketFlow 没有任何第三方依赖，安装后即可直接使用，不会影响你现有的项目环境。
:::

### 1.3 第一个 Flow：Hello PocketFlow

```python
from pocketflow import Node, Flow

class GreetNode(Node):
    def prep(self, shared):
        return shared.get("name", "World")

    def exec(self, name):
        return f"Hello, {name}! Welcome to PocketFlow."

    def post(self, shared, prep_res, exec_res):
        shared["greeting"] = exec_res
        print(exec_res)

# 构建并运行
greet = GreetNode()
flow = Flow(start=greet)
flow.run({"name": "小明"})
# 输出：Hello, 小明! Welcome to PocketFlow.
```

### 1.4 配套示例代码

本教程的所有代码示例都已整理为**完整可运行的 Python 脚本**，存放在 [`examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-intro/examples) 文件夹中：

| 文件 | 对应章节 | 核心概念 |
| :--- | :--- | :--- |
| `01_hello_pocketflow.py` | 1.3 第一个 Flow | Node + Flow 基础用法 |
| `02_node_lifecycle.py` | 2.1 Node 最小单元 | prep → exec → post 三阶段 |
| `03_flow_chain.py` | 2.2 & 2.3 图执行 | `>>` 链式连接 |
| `04_conditional_flow.py` | 2.3 条件连接 | `- "action" >>` 条件分支 |
| `05_shared_store.py` | 3 通信机制 | 节点间数据传递 |
| `06_retry_node.py` | 5.2 重试机制 | max_retries、exec_fallback |
| `07_nested_flow.py` | 5.3 嵌套子流程 | Flow 作为节点 |
| `08_batch_node.py` | 5.4 批量处理 | BatchNode |
| `09_async_parallel.py` | 5.6 异步家族 | AsyncParallelBatchNode |
| `10_loop_pattern.py` | 4 设计模式 | 循环/自校正 |

::: code-group

```bash [一键运行]
cd examples
pip install -r requirements.txt
python 01_hello_pocketflow.py
```

```bash [按顺序学习]
cd examples
pip install -r requirements.txt
python 01_hello_pocketflow.py
python 02_node_lifecycle.py
python 03_flow_chain.py
# ... 依次运行
```

:::

::: info 关于示例代码
- 所有示例**自包含**，不需要 API 密钥或外部服务
- LLM 调用使用模拟逻辑代替，便于理解核心机制
- 如需接入真实 LLM，只需替换 `exec()` 中的模拟逻辑即可
:::

---

## 2. 核心抽象：只有两个概念

PocketFlow 的全部设计可以用一句话概括：

> **Node**（节点）负责"做事"，**Flow**（流程）负责"调度"。

就这两个概念，没有更多了。

### 2.1 Node —— 执行的最小单元

每个 Node 都遵循**三阶段执行模型**：

```
prep(shared)  →  exec(prep_res)  →  post(shared, prep_res, exec_res)
  准备数据          执行逻辑           后处理 & 决策
```

- **prep**：从共享存储 `shared` 中**读取**所需数据
- **exec**：执行核心业务逻辑（如调用 LLM API）
- **post**：将结果**写回** `shared`，并返回一个 `action` 字符串

<NodeLifecycleDemo />

::: tip 为什么要分三个阶段？
分三阶段的好处在于**解耦**：
- `prep` 和 `post` 负责和外部世界（shared）交互
- `exec` 是纯粹的业务逻辑，完全不知道 shared 的存在
- 这让 `exec` 可以被独立测试、独立重试、独立替换
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

::: info 这里发生了什么？
- `>>` 重载了 `__rshift__` 方法，调用 `self.next(other, "default")`
- `-` 重载了 `__sub__` 方法，返回一个 `_ConditionalTransition` 对象
- `_ConditionalTransition` 的 `>>` 再调用 `src.next(tgt, action)`
- 两层操作符重载，实现了直观的图构建语法
:::

### 2.4 形式化视角：PocketFlow 即有限状态自动机

::: details 💡 可选阅读 —— 本节从理论角度解析 PocketFlow，不影响后续学习。如果你只想快速上手，可以跳过直接进入 [§3 通信机制](#_3-通信机制-shared-store-与-params)。
:::

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

不同 LLM 应用模式，实际上对应不同形态的自动机：

```text
聊天机器人 —— 带自环的单状态自动机
┌──── "continue" ────┐
│                     │
▼                     │
●  ChatNode ──────────┘
     │ (None)
     ▼
   [结束]

搜索智能体 —— 有分支 + 环的自动机
          "need_more"
  ┌──── Think ────────▶ Search ──┐
  │       │                      │
  │       │ "enough"    "default"│
  │       ▼                      │
  │   Synthesize                 │
  │       │ (None)               │
  │       ▼                      │
  │     [结束]                   │
  └──────────────────────────────┘

结构化输出 —— 带回退边的自动机
  Generate ──▶ Validate ──▶ Check
                              │ │
                  "retry" ◀───┘ │ "done"
                  (回到 Generate) ▼
                              Output
```

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

---

## 3. 通信机制：Shared Store 与 Params

PocketFlow 提供**两种**节点间通信方式，各有分工。

### 3.1 Shared Store —— 全局共享字典

节点之间**不直接通信**，而是通过一个共享的 `shared` 字典来传递数据。

```python
shared = {}

# Node A 的 post() 写入数据
shared["question"] = "什么是 PocketFlow？"

# Node B 的 prep() 读取数据
question = shared["question"]
```

::: warning 设计哲学
为什么不让节点直接传参？因为 PocketFlow 追求**最小抽象**：
- `shared` 是一个普通 Python 字典，没有任何封装
- 所有节点都能读写，足够灵活
- 你完全清楚数据从哪来、到哪去，没有"黑魔法"
:::

### 3.2 Params —— 局部参数传递

除了 `shared` 这个"全局共享"机制，PocketFlow 还提供了一套**局部参数**机制 —— `params`。

```python
# 设置节点参数
node.set_params({"filename": "doc1.txt"})

# 在节点中读取参数
class ProcessFile(Node):
    def prep(self, shared):
        filename = self.params["filename"]  # 读取局部参数
        return shared["files"][filename]
```

Params 的值由**父 Flow 传入**：当 Flow 执行子节点时，会自动调用 `node.set_params(params)` 将参数传递给每个节点。这在 **BatchFlow**（见第 5.5 节）中尤为关键 —— BatchFlow 每次迭代会将不同的 params 传递给子节点，让同一条 Flow 用不同参数运行多次。

::: tip Shared 与 Params 的类比
可以用编程中的内存模型来理解这两种通信方式：
- **Shared Store** 像**堆（Heap）**—— 所有函数（节点）共享同一块内存，任意读写
- **Params** 像**栈（Stack）**—— 由调用者（父 Flow）赋值，节点内只读

| 特性 | Shared Store | Params |
| :--- | :--- | :--- |
| 作用域 | 全局，所有节点共享 | 局部，由父 Flow 传入 |
| 用途 | 存储数据、结果、大对象 | 传递任务标识（文件名、ID） |
| 可变性 | 节点可读写 | 节点内只读 |
| 典型场景 | 对话历史、检索结果 | BatchFlow 的迭代参数 |
:::

---

## 4. 六大设计模式

掌握了 Node 和 Flow，你就可以构建 LLM 应用中几乎所有的主流模式。它们不是框架提供的"功能类"，而是 Node + Flow 自然组合出的**图拓扑**：

| 模式 | 图形态 | 关键技巧 | 对应案例 |
| :--- | :--- | :--- | :--- |
| **链式调用** | A → B → C 顺序执行 | `a >> b >> c` | [写作工作流](../pocketflow-cases/#_2-写作工作流-writing-workflow) |
| **条件分支** | 根据结果走不同路径 | `node - "action" >> target` | [搜索智能体](../pocketflow-cases/#_4-搜索智能体) |
| **循环/重试** | 不满意则重做 | `post()` 返回 action 指回前序节点 | [聊天机器人](../pocketflow-cases/#_1-聊天机器人-chatbot) |
| **嵌套子流程** | Flow 中包含子 Flow | Flow 继承自 BaseNode | [多智能体协作](../pocketflow-cases/#_5-多智能体协作) |
| **批量处理** | 列表中的每个元素独立处理 | BatchNode / BatchFlow | [Map-Reduce](../pocketflow-cases/#_6-map-reduce-批处理) |
| **并行执行** | 多个任务同时运行 | AsyncParallelBatchNode | [并行处理](../pocketflow-cases/#_7-并行处理-8x-加速) |

每种模式的代码骨架：

```python
# 链式：顺序执行
a >> b >> c
flow = Flow(start=a)

# 条件分支：根据 action 走不同路径
check - "yes" >> handle_yes
check - "no"  >> handle_no
flow = Flow(start=check)

# 循环：post() 返回 action 指回前序节点
step >> verify
verify - "retry" >> step        # 不满意则重做
verify - "done"  >> output      # 满意则输出

# 嵌套子流程：Flow 本身也是 BaseNode
sub_flow = Flow(start=sub_a)
main_a >> sub_flow >> main_b    # Flow 当节点用

# 批量处理：BatchNode 自动遍历列表
class ProcessAll(BatchNode):
    def prep(self, shared): return shared["items"]  # 返回列表
    def exec(self, item): return process(item)       # 逐一执行

# 并行执行：asyncio.gather 并发
class ParallelProcess(AsyncParallelBatchNode):
    async def prep_async(self, shared): return shared["items"]
    async def exec_async(self, item): return await async_process(item)
```

<el-alert title="关键洞察" type="success" show-icon>
PocketFlow 没有为每种模式创建专门的类 —— 它们都是 Node + Flow + 操作符重载的<strong>自然组合</strong>。这就是 100 行代码能覆盖这么多场景的原因。
</el-alert>

---

## 5. 深入源码：100 行的全部秘密

<CoreCodeDemo />

PocketFlow 的 100 行源码包含 **12 个类**，构成以下层次结构：

```
BaseNode                          ← 万物之基（params / successors / 三阶段 / 操作符重载）
├── Node(BaseNode)                ← 可重试的执行单元（max_retries / wait / exec_fallback）
│   ├── BatchNode(Node)           ← 批量处理节点（对列表逐一执行 exec）
│   └── AsyncNode(Node)           ← 异步节点（async 版三阶段）
│       ├── AsyncBatchNode        ← 顺序异步批处理
│       └── AsyncParallelBatchNode← 并行异步批处理（asyncio.gather）
├── Flow(BaseNode)                ← 图执行引擎（遍历有向图）
│   ├── BatchFlow(Flow)           ← 批量运行整条 Flow（不同 params）
│   └── AsyncFlow(Flow, AsyncNode)← 异步图执行引擎（支持混合同步/异步节点）
│       ├── AsyncBatchFlow        ← 顺序异步批量 Flow
│       └── AsyncParallelBatchFlow← 并行异步批量 Flow
└── _ConditionalTransition        ← 辅助类（实现 - "action" >> 语法）
```

下面逐一解读关键类。

### 5.1 BaseNode —— 万物之基

BaseNode 是所有节点和流程的基类，它定义了：

- **`params` 字典**：存储节点的配置参数（由父 Flow 传入）
- **`successors` 字典**：存储 `action → 后继节点` 的映射
- **三阶段方法**：`prep()`、`exec()`、`post()`
- **操作符重载**：`>>`（默认连接）和 `-`（条件连接）

### 5.2 Node —— 可重试的执行单元

Node 继承 BaseNode，增加了**重试机制**：

```python
class Node(BaseNode):
    def __init__(self, max_retries=1, wait=0):
        self.max_retries = max_retries
        self.wait = wait

    def exec_fallback(self, prep_res, exc):
        raise exc  # 默认：重新抛出异常

    def _exec(self, prep_res):
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res, e)
                if self.wait > 0:
                    time.sleep(self.wait)
```

::: tip 实用场景
当调用 LLM API 时，网络波动、限流等问题很常见。设置 `max_retries=3, wait=2` 就能最多尝试 3 次（首次 + 2 次重试），每次间隔 2 秒。所有重试耗尽后，`exec_fallback(prep_res, exc)` 会被调用 —— 你可以覆写它来返回降级结果而非抛出异常。
:::

### 5.3 Flow —— 图执行引擎

Flow 本身也是 BaseNode 的子类 —— 这意味着 **Flow 可以嵌套在其他 Flow 中**，这是构建复杂应用的关键。

```python
class Flow(BaseNode):
    def _orch(self, shared, params=None):
        curr = copy.copy(self.start_node)
        p = params or {**self.params}
        while curr:
            curr.set_params(p)          # 将 params 传给每个子节点
            last_action = curr._run(shared)
            curr = copy.copy(self.get_next_node(curr, last_action))
        return last_action
```

注意 `curr.set_params(p)` —— Flow 在执行每个子节点前，都会将自身的 params 传递给子节点。这就是第 3.2 节 Params 机制的运作方式。

```python
# 子 Flow 作为一个 Node 参与到父 Flow 中
sub_flow = Flow(start=sub_start_node)
main_start >> sub_flow >> main_end
main_flow = Flow(start=main_start)
```

### 5.4 BatchNode —— 批量处理

BatchNode 只覆写了一个方法，就实现了批处理：

```python
class BatchNode(Node):
    def _exec(self, items):
        return [super()._exec(i) for i in (items or [])]
```

- `prep()` 返回一个列表
- `exec()` 对列表中每个元素**独立执行**
- 每个元素独享 Node 的重试机制

### 5.5 BatchFlow —— 批量运行整条 Flow

BatchFlow 与 BatchNode 解决不同的问题：BatchNode 在**一个节点内**批量处理列表元素，而 BatchFlow 用**不同的 params 多次运行整条 Flow**。

```python
class BatchFlow(Flow):
    def _run(self, shared):
        pr = self.prep(shared) or []        # prep 返回 params 字典列表
        for bp in pr:
            self._orch(shared, {**self.params, **bp})  # 合并父级 params 与当前批次 params
        return self.post(shared, pr, None)
```

**使用方式**：

```python
class SummarizeAllFiles(BatchFlow):
    def prep(self, shared):
        filenames = list(shared["files"].keys())
        return [{"filename": fn} for fn in filenames]  # 每次迭代一个文件

class SummarizeFile(Node):
    def prep(self, shared):
        filename = self.params["filename"]      # 通过 params 获取当前文件名
        return shared["files"][filename]

    def exec(self, content):
        return call_llm(f"Summarize: {content}")

    def post(self, shared, prep_res, exec_res):
        shared["summaries"][self.params["filename"]] = exec_res

# 构建 Flow
summarize = SummarizeFile()
inner_flow = Flow(start=summarize)
batch_flow = SummarizeAllFiles(start=inner_flow)
batch_flow.run(shared)
```

::: tip BatchNode vs BatchFlow
- **BatchNode**：一个节点，批量执行 `exec()` → 适合"对列表每项做同一个操作"
- **BatchFlow**：一条完整 Flow，用不同参数多次运行 → 适合"对多个任务运行同一条流水线"
:::

### 5.6 AsyncNode 与异步家族

AsyncNode 提供三阶段执行的 `async/await` 版本：

```python
class AsyncNode(Node):
    async def prep_async(self, shared): pass
    async def exec_async(self, prep_res): pass
    async def exec_fallback_async(self, prep_res, exc): raise exc
    async def post_async(self, shared, prep_res, exec_res): pass

    def _run(self, shared):
        raise RuntimeError("Use run_async.")  # 不能在同步 Flow 中使用！
```

::: danger 关键约束
- AsyncNode 的 `_run()` 会**直接抛出 RuntimeError** —— 它**不能**放在普通 `Flow` 中
- AsyncNode **必须**包裹在 `AsyncFlow` 中运行
- 反过来，`AsyncFlow` **可以**包含普通同步 Node（它会自动判断用 `_run` 还是 `_run_async`）
:::

基于 AsyncNode，PocketFlow 提供了一系列异步组合类：

| 类 | 继承关系 | 行为 |
| :--- | :--- | :--- |
| **AsyncNode** | Node | 异步三阶段执行 |
| **AsyncBatchNode** | AsyncNode + BatchNode | 异步逐个处理列表元素（`for` + `await`） |
| **AsyncParallelBatchNode** | AsyncNode + BatchNode | 异步**并行**处理列表元素（`asyncio.gather`） |
| **AsyncFlow** | Flow + AsyncNode | 异步图引擎，支持混合同步/异步节点 |
| **AsyncBatchFlow** | AsyncFlow + BatchFlow | 异步逐次运行多组 params |
| **AsyncParallelBatchFlow** | AsyncFlow + BatchFlow | 异步**并行**运行多组 params（`asyncio.gather`） |

其中 `AsyncParallelBatchNode` 是最常用的 —— 在 I/O 密集场景（多个 API 调用、多文件处理）下，`asyncio.gather()` 可以获得**数倍的性能提升**：

```python
class AsyncParallelBatchNode(AsyncNode, BatchNode):
    async def _exec(self, items):
        return await asyncio.gather(
            *(super()._exec(i) for i in items)
        )
```

---

## 6. 工具函数层：Node 里装什么？

前面 5 章讲的都是 PocketFlow **框架本身** —— Node 生命周期、Flow 图遍历、通信机制、设计模式、源码实现。但 PocketFlow 是纯编排框架，**不包含任何具体实现**。那么 Node 的 `exec()` 里到底填什么？

答案是**工具函数**（Utility Functions）—— 你自己编写或引入的外部能力：

| 工具函数类别 | 用途 | 常见选择 |
| :--- | :--- | :--- |
| **LLM 调用** | 文本生成、分析、决策 | OpenAI / Claude / 本地模型 |
| **Web 搜索** | 获取实时信息 | Google / Bing / DuckDuckGo |
| **文本切片** | 将长文档拆成小块 | 按段落 / 按 token 数 / 递归拆分 |
| **Embedding** | 将文本转为向量 | OpenAI / HuggingFace / 本地模型 |
| **向量数据库** | 存储和检索向量 | Pinecone / FAISS / Chroma |
| **语音合成** | 文本转语音 | TTS API |
| **可视化与调试** | 追踪 Flow 执行过程 | 日志 / 追踪工具 |

```python
# 典型的工具函数：LLM 调用封装
def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

# 在 Node 的 exec() 中调用
class AnalyzeNode(Node):
    def exec(self, data):
        return call_llm(f"请分析：{data}")  # 工具函数填进 exec()
```

::: tip 工具函数 vs 设计模式
- **设计模式**（§4）= 图拓扑，决定节点之间**怎么连**
- **工具函数**（本节）= 节点内部，决定每个节点**做什么**

两者正交：同一个 LLM 调用工具可以用在链式工作流里，也可以用在 智能体 循环里。PocketFlow 不限制你用什么工具，你可以自由组合。
:::

更进一步，工具函数也可以被**模块化为技能文件**（Markdown），智能体 在运行时动态选择并注入 prompt —— 这就是 **智能体技能** 模式。详见 [应用案例第 12 节：智能体技能](../pocketflow-cases/#_12-智能体技能-技能路由)。

---

## 7. 开发者体验：Agentic Coding

PocketFlow 推崇一种高效的人机协作开发范式 —— **Agentic Coding**：

> **人类负责设计架构**（定义 Node、画 Flow 图、设计 shared 数据契约），**AI 负责写实现代码**（填充 `exec()` 方法体）。

为什么 PocketFlow 特别适合这种模式？

- **核心极简**：AI 只需理解 Node 和 Flow 两个概念
- **接口清晰**：每个 Node 的输入输出都通过 shared 明确定义
- **零依赖**：不需要理解复杂的第三方 API
- **可测试**：每个 Node 的 `exec()` 可以独立测试

::: info 完整方法论
Agentic Coding 包含 8 个步骤：需求澄清 → Flow 设计 → Utilities 识别 → Data 契约 → Node 设计 → 实现 → 优化 → 可靠性。完整的流程讲解、设计文档模板和可运行示例代码，请参考 [应用案例第 11 节：智能体编程](../pocketflow-cases/#_11-智能体编程-agentic-coding)。
:::

---

## 8. 名词速查表 (Glossary)

| 名词 | 全称 | 解释 |
| :--- | :--- | :--- |
| **Node** | Node | **执行的最小单元**。包含 prep → exec → post 三阶段生命周期。 |
| **Flow** | Flow | **图执行引擎**。从 start_node 开始，沿 action 遍历有向图。 |
| **shared** | Shared Store | **全局共享字典**。节点间通信的主要渠道，所有 Node 都能读写。 |
| **params** | Parameters | **局部参数字典**。由父 Flow 传入，节点通过 `self.params` 读取，适合传递任务标识。 |
| **action** | Action String | **路由标签**。post() 返回的字符串，Flow 据此决定下一个节点。 |
| **BatchNode** | Batch Node | **批处理节点**。对列表中每个元素独立执行 exec()。 |
| **BatchFlow** | Batch Flow | **批量流程**。用不同 params 多次运行整条 Flow。 |
| **AsyncNode** | Async Node | **异步节点**。提供 async/await 版本的三阶段方法，必须在 AsyncFlow 中运行。 |
| **AsyncFlow** | Async Flow | **异步图引擎**。支持混合同步/异步节点的异步版 Flow。 |
| **prep** | Preparation | **准备阶段**。从 shared 读取数据，传给 exec。 |
| **exec** | Execution | **执行阶段**。核心业务逻辑，不直接访问 shared。 |
| **post** | Post-processing | **后处理阶段**。将结果写回 shared，返回 action。 |
| **exec_fallback** | Execution Fallback | **降级回调**。所有重试耗尽后调用，可覆写以返回兜底结果。 |

---

### 下一步

- 前往 [PocketFlow 应用案例](../pocketflow-cases/) 学习实战案例
- 访问 [PocketFlow GitHub](https://github.com/The-Pocket/PocketFlow) 查看完整 cookbook
