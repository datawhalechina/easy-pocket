---
title: '深入源码：100 行的全部秘密'
description: 'PocketFlow 12 个类的继承体系：BaseNode、Node、Flow、BatchNode、BatchFlow、AsyncNode 全解析。'
---

# 5. 深入源码：100 行的全部秘密

<CoreCodeDemo />

PocketFlow 的 100 行源码包含 **12 个类**，构成以下层次结构：

```
BaseNode                                       ← 万物之基（params / successors / 三阶段 / 操作符重载）
├── Node(BaseNode)                             ← 可重试的执行单元（max_retries / wait / exec_fallback）
│   ├── BatchNode(Node)                        ← 批量处理节点（对列表逐一执行 exec）
│   └── AsyncNode(Node)                        ← 异步节点（async 版三阶段）
│       ├── AsyncBatchNode(AsyncNode, BatchNode)        ← 顺序异步批处理 ◆
│       └── AsyncParallelBatchNode(AsyncNode, BatchNode)← 并行异步批处理 ◆
├── Flow(BaseNode)                             ← 图执行引擎（遍历有向图）
│   ├── BatchFlow(Flow)                        ← 批量运行整条 Flow（不同 params）
│   └── AsyncFlow(Flow, AsyncNode)             ← 异步图执行引擎（混合同步/异步节点）◆
│       ├── AsyncBatchFlow(AsyncFlow, BatchFlow)        ← 顺序异步批量 Flow ◆
│       └── AsyncParallelBatchFlow(AsyncFlow, BatchFlow)← 并行异步批量 Flow ◆
└── _ConditionalTransition                     ← 辅助类（实现 - "action" >> 语法）
```

::: info ◆ 菱形继承（Diamond Inheritance）
标记 ◆ 的类同时继承两个父类，形成菱形继承。例如 `AsyncBatchNode(AsyncNode, BatchNode)` —— 从 AsyncNode 获得 async 能力，从 BatchNode 获得批量循环，Python 的方法解析顺序（Method Resolution Order, MRO）确保 `_exec()` 等方法的调用顺序正确。这种"能力叠加"设计让 12 个类覆盖了所有同步/异步 × 单个/批量 × 顺序/并行的组合。
:::

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

注意源码中 `for self.cur_retry in range(self.max_retries)` —— 重试计数器 `self.cur_retry` 是节点实例属性，你可以在 `exec()` 中读取它（`self.cur_retry`）来判断当前是第几次重试，从而在不同重试轮次采用不同策略。
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

**三个关键细节：**

**1. `copy.copy` —— 防止状态泄漏**

注意 `_orch` 中的 `copy.copy(self.start_node)` 和 `copy.copy(self.get_next_node(...))`。每次执行都对节点做浅拷贝，这意味着**同一条 Flow 可以安全地多次运行**，每次运行使用独立的节点副本，不会因上一次运行残留的 `params`、`cur_retry` 等内部状态而互相干扰。

**2. Flow 自身也有 prep/post 生命周期**

Flow 继承自 BaseNode，因此它的 `_run()` 实际上是 `prep → _orch → post`。大多数时候你不需要覆写 Flow 的 `prep/post`，但 **BatchFlow 正是利用了这一点** —— 它覆写 `prep()` 返回 params 列表，再在 `_run()` 中逐一迭代（见 [§5.5](#_5-5-batchflow-——-批量运行整条-flow)）。

**3. `Flow.post` 默认透传 last_action**

源码中 `Flow.post()` 被覆写为 `return exec_res`，即把最后一个节点的 action 原样返回。这使得**嵌套 Flow 可以参与父 Flow 的路由** —— 子 Flow 内部最后一个节点返回的 action 会传递给父 Flow，决定父 Flow 的下一跳。

注意 `curr.set_params(p)` —— Flow 在执行每个子节点前，都会将自身的 params 传递给子节点。这就是[第 3.2 节](./communication-and-patterns#_3-2-params-——-局部参数传递) Params 机制的运作方式。

::: warning get_next_node 的优雅终止
`post()` 返回的 action 如果在 `successors` 中找不到匹配，Flow **不会崩溃** —— 它会发出一条 warning 并正常结束。这意味着：
- 返回 `None`（即 `post()` 没有显式 return）→ 如果没有 `"default"` 后继，Flow 结束
- 返回一个未注册的 action → Flow 发出警告并结束
- 这是**有意为之**的设计，让流程终止变得简单自然
:::

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

::: tip 为什么需要 async？
本教程的案例使用同步模拟函数来降低门槛，但**真实业务几乎都是异步的**。LLM API 调用（OpenAI、Claude）、Web 搜索、数据库查询都是网络 I/O —— 每次请求要等几百毫秒到几秒。同步代码在等待期间阻塞整个线程；async/await 让 Python 在等待 I/O 时去处理其他任务。

生产环境中，你几乎总是用 `AsyncNode` + `AsyncFlow` 替代 `Node` + `Flow`。接口完全对称，只需给方法加上 `async` 前缀和 `_async` 后缀，逻辑代码不变。
:::

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

AsyncFlow 是如何做到"混合同步/异步节点"的？关键在 `_orch_async` 的一行 `isinstance` 检测：

```python
# AsyncFlow._orch_async 核心逻辑（简化）
while curr:
    if isinstance(curr, AsyncNode):
        last_action = await curr._run_async(shared)   # 异步节点
    else:
        last_action = curr._run(shared)                # 普通同步节点
    curr = self.get_next_node(curr, last_action)
```

这意味着你可以在一条 AsyncFlow 中自由混搭同步和异步节点 —— AsyncFlow 会自动为每个节点选择正确的调用方式。

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
