---
title: '通信机制与设计模式'
description: 'Shared Store 全局共享与 Params 局部参数，以及 PocketFlow 的六大设计模式。'
---

# 3. 通信机制：Shared Store 与 Params

PocketFlow 提供**两种**节点间通信方式，各有分工。

### 3.1 Shared Store —— 全局共享字典

<div align="center"><img src="/easy-pocket/shared.png" width="420"/></div>

*Shared Store：所有节点通过共享字典读写数据*

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

Params 的值由**父 Flow 传入**：当 Flow 执行子节点时，会自动调用 `node.set_params(params)` 将参数传递给每个节点。这在 **BatchFlow**（见[第 5.5 节](./source-code#_5-5-batchflow-——-批量运行整条-flow)）中尤为关键 —— BatchFlow 每次迭代会将不同的 params 传递给子节点，让同一条 Flow 用不同参数运行多次。

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


# 4. 六大设计模式

掌握了 Node 和 Flow，你就可以构建 LLM 应用中几乎所有的主流模式。它们不是框架提供的"功能类"，而是 Node + Flow 自然组合出的**图拓扑**：

| 模式 | 图形态 | 关键技巧 | 对应案例 |
| :--- | :--- | :--- | :--- |
| **链式调用** | A → B → C 顺序执行 | `a >> b >> c` | [写作工作流](../pocketflow-cases/beginner#_2-写作工作流-writing-workflow) |
| **条件分支** | 根据结果走不同路径 | `node - "action" >> target` | [搜索智能体](../pocketflow-cases/agents#_4-搜索智能体) |
| **循环/重试** | 不满意则重做 | `post()` 返回 action 指回前序节点 | [聊天机器人](../pocketflow-cases/beginner#_1-聊天机器人-chatbot) |
| **嵌套子流程** | Flow 中包含子 Flow | Flow 继承自 BaseNode | [多智能体协作](../pocketflow-cases/agents#_5-多智能体协作) |
| **批量处理** | 列表中的每个元素独立处理 | BatchNode / BatchFlow | [Map-Reduce](../pocketflow-cases/batch-and-parallel#_6-map-reduce-批处理) |
| **并行执行** | 多个任务同时运行 | AsyncParallelBatchNode | [并行处理](../pocketflow-cases/batch-and-parallel#_7-并行处理-8x-加速) |

每种模式的代码骨架：

<div align="center"><img src="/easy-pocket/workflow.png" width="380"/></div>

*链式调用：节点按顺序依次执行*

```python
# 链式：顺序执行
a >> b >> c
flow = Flow(start=a)
```

<div align="center"><img src="/easy-pocket/branch.png" width="380"/></div>

*条件分支：根据 action 走不同路径*

```python
# 条件分支：根据 action 走不同路径
check - "yes" >> handle_yes
check - "no"  >> handle_no
flow = Flow(start=check)
```

<div align="center"><img src="/easy-pocket/looping.png" width="380"/></div>

*循环/重试：不满足条件则持续推理*

```python
# 循环：post() 返回 action 指回前序节点
step >> verify
verify - "retry" >> step        # 不满意则重做
verify - "done"  >> output      # 满意则输出
```

<div align="center"><img src="/easy-pocket/nesting.png" width="420"/></div>

*嵌套子流程：Flow 作为可复用的步骤*

```python
# 嵌套子流程：Flow 本身也是 BaseNode
sub_flow = Flow(start=sub_a)
main_a >> sub_flow >> main_b    # Flow 当节点用
```

<div align="center"><img src="/easy-pocket/batch.png" width="380"/></div>

*批量处理：对列表中每个元素重复执行*

```python
# 批量处理：BatchNode 自动遍历列表
class ProcessAll(BatchNode):
    def prep(self, shared): return shared["items"]  # 返回列表
    def exec(self, item): return process(item)       # 逐一执行
```

<div align="center"><img src="/easy-pocket/parallel.png" width="380"/></div>

*并行执行：多个任务并发处理*

```python
# 并行执行：asyncio.gather 并发
class ParallelProcess(AsyncParallelBatchNode):
    async def prep_async(self, shared): return shared["items"]
    async def exec_async(self, item): return await async_process(item)
```

<el-alert title="关键洞察" type="success" show-icon>
PocketFlow 没有为每种模式创建专门的类 —— 它们都是 Node + Flow + 操作符重载的<strong>自然组合</strong>。这就是 100 行代码能覆盖这么多场景的原因。
</el-alert>
