---
title: 'PocketFlow 原理入门 —— 100 行代码的极简 LLM 框架'
description: '从零理解 PocketFlow 的核心原理：Node 三阶段模型、Flow 图执行、Batch 批处理与 Async 异步并发。'
---

# PocketFlow 原理入门 (Interactive Intro to PocketFlow)

> **学习指南**：本章节不需要编程基础，通过交互式演示带你了解 PocketFlow —— 一个仅 100 行代码、零依赖的 LLM 应用框架。从"它能做什么"讲起，一直到"它是怎么做到的"。

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

---

## 1. 核心抽象：只有两个概念

PocketFlow 的全部设计可以用一句话概括：

> **Node**（节点）负责"做事"，**Flow**（流程）负责"调度"。

就这两个概念，没有更多了。

### 1.1 Node —— 执行的最小单元

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

### 1.2 Flow —— 图编排引擎

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

### 1.3 连接节点的两种方式

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

---

## 2. Shared：节点间的通信机制

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

---

## 3. 深入源码：100 行的全部秘密

<CoreCodeDemo />

### 3.1 BaseNode —— 万物之基

BaseNode 是所有节点和流程的基类，它定义了：

- **`params` 字典**：存储节点的配置参数
- **`successors` 字典**：存储 `action → 后继节点` 的映射
- **三阶段方法**：`prep()`、`exec()`、`post()`
- **操作符重载**：`>>`（默认连接）和 `-`（条件连接）

### 3.2 Node —— 可重试的执行单元

Node 继承 BaseNode，增加了**重试机制**：

```python
class Node(BaseNode):
    def __init__(self, max_retries=1, wait=0):
        self.max_retries = max_retries
        self.wait = wait

    def _exec(self, prep_res):
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res, e)
                time.sleep(self.wait)
```

::: tip 实用场景
当调用 LLM API 时，网络波动、限流等问题很常见。设置 `max_retries=3, wait=2` 就能自动重试 3 次，每次间隔 2 秒。
:::

### 3.3 Flow —— 图执行引擎

Flow 本身也是 BaseNode 的子类 —— 这意味着 **Flow 可以嵌套在其他 Flow 中**，这是构建复杂应用的关键。

```python
# 子 Flow 作为一个 Node 参与到父 Flow 中
sub_flow = Flow(start=sub_start_node)
main_start >> sub_flow >> main_end
main_flow = Flow(start=main_start)
```

### 3.4 BatchNode —— 批量处理

BatchNode 只覆写了一个方法，就实现了批处理：

```python
class BatchNode(Node):
    def _exec(self, items):
        return [super()._exec(i) for i in (items or [])]
```

- `prep()` 返回一个列表
- `exec()` 对列表中每个元素**独立执行**
- 每个元素独享 Node 的重试机制

### 3.5 AsyncNode —— 异步并发

AsyncNode 提供 `async/await` 版本的三阶段执行。配合 `AsyncParallelBatchNode`，可以用 `asyncio.gather()` 实现**真正的并发**：

```python
class AsyncParallelBatchNode(AsyncNode):
    async def _exec(self, items):
        return await asyncio.gather(
            *(super()._exec(i) for i in items)
        )
```

这在调用多个 API、处理多个文件等 I/O 密集场景下，可以获得**数倍的性能提升**。

---

## 4. 六大设计模式

掌握了 Node 和 Flow，你就可以构建 LLM 应用中几乎所有的主流模式：

| 模式 | 说明 | 关键技巧 |
| :--- | :--- | :--- |
| **链式调用** | A → B → C 顺序执行 | `a >> b >> c` |
| **条件分支** | 根据结果走不同路径 | `node - "action" >> target` |
| **循环/重试** | 不满意则重做 | `post()` 返回 action 指回前序节点 |
| **嵌套子流程** | Flow 中包含子 Flow | Flow 继承自 BaseNode |
| **批量处理** | 列表中的每个元素独立处理 | BatchNode / BatchFlow |
| **并行执行** | 多个任务同时运行 | AsyncParallelBatchNode |

<el-alert title="关键洞察" type="success" show-icon>
PocketFlow 没有为每种模式创建专门的类 —— 它们都是 Node + Flow + 操作符重载的<strong>自然组合</strong>。这就是 100 行代码能覆盖这么多场景的原因。
</el-alert>

---

## 5. 开发者体验：Agentic Coding

PocketFlow 推崇一种新的开发范式 —— **Agentic Coding**：

> **人类负责设计架构**（定义 Node、画 Flow 图），**AI 负责写实现代码**（填充 `exec()` 方法体）。

### 5.1 为什么 PocketFlow 适合 Agentic Coding？

1. **核心极简**：AI 只需理解 Node 和 Flow 两个概念
2. **接口清晰**：每个 Node 的输入输出都通过 shared 明确定义
3. **零依赖**：不需要理解复杂的第三方 API
4. **可测试**：每个 Node 的 exec() 可以独立测试

### 5.2 推荐开发流程

<ClientOnly>
  <StepBar
    :active="4"
    :items="[
      { title: '画架构图', description: '确定有哪些 Node、如何连接' },
      { title: '定义 shared', description: '确定节点间传递的数据结构' },
      { title: 'AI 填充 exec()', description: '让 AI 实现每个节点的核心逻辑' },
      { title: '测试 & 迭代', description: '运行 Flow，根据结果调整' },
      { title: '部署', description: '打包为 API 服务或脚本' }
    ]"
  />
</ClientOnly>

---

## 6. 快速上手

### 6.1 环境配置

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

### 6.2 安装 PocketFlow

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

### 6.3 第一个 Flow：Hello PocketFlow

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

### 6.4 配套示例代码

本教程的所有代码示例都已整理为**完整可运行的 Python 脚本**，存放在 [`examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-intro/examples) 文件夹中：

| 文件 | 对应章节 | 核心概念 |
| :--- | :--- | :--- |
| `01_hello_pocketflow.py` | 6.3 第一个 Flow | Node + Flow 基础用法 |
| `02_node_lifecycle.py` | 1.1 Node 最小单元 | prep → exec → post 三阶段 |
| `03_flow_chain.py` | 1.2 & 1.3 图执行 | `>>` 链式连接 |
| `04_conditional_flow.py` | 1.3 条件连接 | `- "action" >>` 条件分支 |
| `05_shared_store.py` | 2 Shared 通信 | 节点间数据传递 |
| `06_retry_node.py` | 3.2 重试机制 | max_retries、exec_fallback |
| `07_nested_flow.py` | 3.3 嵌套子流程 | Flow 作为节点 |
| `08_batch_node.py` | 3.4 批量处理 | BatchNode |
| `09_async_parallel.py` | 3.5 异步并发 | AsyncParallelBatchNode |
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

## 7. 名词速查表 (Glossary)

| 名词 | 全称 | 解释 |
| :--- | :--- | :--- |
| **Node** | Node | **执行的最小单元**。包含 prep → exec → post 三阶段生命周期。 |
| **Flow** | Flow | **图执行引擎**。从 start_node 开始，沿 action 遍历有向图。 |
| **shared** | Shared Store | **共享字典**。节点间通信的唯一渠道，所有 Node 都能读写。 |
| **action** | Action String | **路由标签**。post() 返回的字符串，Flow 据此决定下一个节点。 |
| **BatchNode** | Batch Node | **批处理节点**。对列表中每个元素独立执行 exec()。 |
| **AsyncNode** | Async Node | **异步节点**。提供 async/await 版本的三阶段方法。 |
| **prep** | Preparation | **准备阶段**。从 shared 读取数据，传给 exec。 |
| **exec** | Execution | **执行阶段**。核心业务逻辑，不直接访问 shared。 |
| **post** | Post-processing | **后处理阶段**。将结果写回 shared，返回 action。 |

---

### 下一步

- 进入 [`examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-intro/examples) 文件夹，动手跑通本章的配套代码
- 前往 [PocketFlow 应用案例](../pocketflow-cases/) 章节，通过 9 个实战案例学习如何构建聊天机器人、RAG、Agent 等应用
- 访问 [PocketFlow GitHub](https://github.com/The-Pocket/PocketFlow) 查看完整 cookbook
