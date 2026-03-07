---
title: '批处理与并行：Map-Reduce、并行处理'
description: 'Map-Reduce 批处理（BatchNode）和并行处理 8x 加速（AsyncParallelBatchNode）的实战案例。'
---

# 批处理与并行

## 6. Map-Reduce 批处理

::: info 难度：入门 | 模式：BatchNode | 关键词：批量评估、数据聚合
:::

### 6.1 架构

<div align="center"><img src="/easy-pocket/map-reduce.png" width="420"/></div>

*Map-Reduce：映射分块 → 批处理 → 规约总结*

Map-Reduce（映射-规约）是最常见的批处理模式 —— 把一批数据"映射"（拆开分别处理），再"规约"（合并结果）。

### 6.2 核心思路

BatchNode 的核心约定：`prep()` 返回一个**列表**，框架自动对列表中的每个元素调用 `exec()`，最后把所有结果收集为列表传给 `post()`。你只需要写"处理单个元素"的逻辑，批量调度由框架完成。

### 6.3 关键代码

下面以"批量评估简历"为例，展示 BatchNode 的三阶段如何配合：

```python
from pocketflow import BatchNode, Flow

class EvalResume(BatchNode):
    """批量评估简历 —— 继承 BatchNode 即可获得批处理能力"""

    def prep(self, shared):
        # prep 返回列表，框架会逐个取出交给 exec
        return shared["resumes"]

    def exec(self, resume):
        # 这里只处理"单份简历"，框架负责循环
        prompt = f"请为以下简历评分(1-10)：\n{resume}"
        score = call_llm(prompt)
        return {"resume": resume, "score": int(score)}

    def post(self, shared, prep_res, exec_res):
        # exec_res 是所有评分结果的列表，与 prep 返回的顺序一致
        shared["scores"] = sorted(
            exec_res, key=lambda x: x["score"], reverse=True
        )
        print(f"Top 3: {shared['scores'][:3]}")

# 构建并运行 Flow
eval_node = EvalResume()
flow = Flow(start=eval_node)
flow.run({"resumes": ["简历A...", "简历B...", "简历C..."]})
```

::: tip 学习要点
- **三阶段约定**：`prep()` 返回列表 → `exec()` 对每个元素独立执行 → `post()` 收到结果列表
- **自动重试**：每个元素的 `exec()` 都有独立的重试机制，单个失败不影响其他元素
- **代码极简**：你只需要写处理单个元素的逻辑，代码量与处理单条数据几乎相同
:::


::: warning 从同步到异步：真实业务的必然选择
上面的 BatchNode 使用同步 `exec()`，适合教学演示。但在真实业务中，LLM API 调用、Web 搜索、数据库查询都是 **I/O 密集型网络请求** —— 每次要等几百毫秒到几秒。同步逐个处理 8 个请求，总耗时 = 8 × 单次；异步并行则可以同时发出，总耗时 ≈ 单次。

PocketFlow 提供三种批处理模式：

| 模式 | 类 | 执行方式 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **同步逐个** | `BatchNode` | `for item: exec(item)` | 教学演示、CPU 密集、需严格顺序 |
| **异步逐个** | `AsyncBatchNode` | `for item: await exec(item)` | API 有速率限制、需要顺序但不阻塞事件循环 |
| **异步并行** | `AsyncParallelBatchNode` | `asyncio.gather(*all)` | **最常用** —— I/O 密集场景，N 倍加速 |

本教程的案例使用同步模拟函数降低入门门槛。接入真实 API 时，只需将 `Node` 换成 `AsyncNode`、`exec()` 换成 `async exec_async()`，逻辑完全不变。
:::

## 7. 并行处理（8x 加速）

::: info 难度：中级 | 模式：AsyncParallelBatchNode | 关键词：并发、I/O 密集
:::

### 7.1 场景

你需要对 8 篇文章分别调用 LLM 生成摘要。同步 BatchNode 每篇等 2 秒，总计 16 秒；用 `AsyncParallelBatchNode` 并行执行，8 篇同时请求，总计约 2 秒 —— **8 倍加速**。

### 7.2 架构

<div align="center"><img src="/easy-pocket/parallel.png" width="380"/></div>

*并行处理：多个任务通过 asyncio.gather() 并发执行*

`AsyncParallelBatchNode` 的执行模型：`prep_async` 返回列表后，所有 `exec_async` 通过 `asyncio.gather()` **同时发出**，最后 `post_async` 收到有序的结果列表。

### 7.3 核心代码

只需继承 `AsyncParallelBatchNode`，将 `exec` 改为 `async exec_async`，框架自动用 `asyncio.gather()` 并行执行所有元素：

```python
import asyncio
from pocketflow import AsyncParallelBatchNode, AsyncFlow

class ParallelProcess(AsyncParallelBatchNode):
    async def prep_async(self, shared):
        return shared["items"]       # 返回待处理列表

    async def exec_async(self, item):
        # 每个 item 并发执行，不互相等待
        result = await async_api_call(item)
        return result

    async def post_async(self, shared, prep_res, exec_res):
        shared["results"] = exec_res  # 结果列表，顺序与输入一致
```

### 7.4 对比：同步 vs 异步并行

下面的对比展示了从 BatchNode 到 AsyncParallelBatchNode 的迁移有多简单 —— 只需改继承类和加 `async/await`：

```python
# 同步方式（案例 6）—— 逐个执行，总耗时 = N × 单次
class SyncProcess(BatchNode):
    def exec(self, item):
        return call_api(item)           # 阻塞等待

# 异步并行（本案例）—— 全部同时发出，总耗时 ≈ 单次
class ParallelProcess(AsyncParallelBatchNode):
    async def exec_async(self, item):
        return await async_api_call(item)  # 非阻塞
```

::: tip 学习要点
- **为什么用异步**：真实 LLM API 都是网络 I/O，天然适合 async/await，同步会白白浪费等待时间
- **接口对称**：BatchNode → AsyncParallelBatchNode，`exec()` → `async exec_async()`，其余逻辑不变
- **结果有序**：`asyncio.gather()` 返回的结果列表与输入顺序一致
- **AsyncFlow**：异步节点必须包裹在 `AsyncFlow` 中运行，不能用普通 `Flow`
- **何时不用并行**：API 有速率限制时，改用 `AsyncBatchNode`（顺序异步），避免被限流
:::
