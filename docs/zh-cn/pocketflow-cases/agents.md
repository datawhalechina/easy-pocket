---
title: '智能体案例：搜索智能体、多智能体协作'
description: '搜索智能体（循环+条件分支）和多智能体协作（AsyncNode+消息队列）的实战案例。'
---

# 智能体案例

## 4. 搜索智能体

::: info 难度：中级 | 模式：循环 + 条件分支 | 关键词：工具调用、自主决策
:::

### 4.1 架构

<div align="center"><img src="/easy-pocket/agent.png" width="420"/></div>

*智能体：循环 + 分支 + 发布/订阅模式*

搜索智能体的核心是 Think → Act → Observe 循环 —— LLM 判断信息是否充足，不够则继续搜索。

### 4.2 核心代码

三个节点分工明确：ThinkNode 决策、SearchNode 执行搜索、SynthesizeNode 整合答案。注意 `post()` 中通过返回不同的 action 字符串来控制 Flow 走向：

```python
class ThinkNode(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "search_results": shared.get("search_results", [])
        }

    def exec(self, data):
        prompt = f"""问题：{data['question']}
已有信息：{data['search_results']}
请决定：还需要搜索什么？输出搜索关键词，或输出 ENOUGH 表示信息充分。"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        if "ENOUGH" in exec_res:
            return "enough"
        shared["search_query"] = exec_res
        return "need_more"

class SearchNode(Node):
    def prep(self, shared):
        return shared["search_query"]

    def exec(self, query):
        return web_search(query)  # 调用搜索 API

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("search_results", []).extend(exec_res)

class SynthesizeNode(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "results": shared["search_results"]
        }

    def exec(self, data):
        prompt = f"基于以下搜索结果回答问题...\n{data}"
        return call_llm(prompt)

# 构建 Flow
think = ThinkNode()
search = SearchNode()
synthesize = SynthesizeNode()

think - "need_more" >> search        # 信息不足则继续搜索
think - "enough" >> synthesize       # 信息充分则生成
search >> think                      # 搜索后回到思考

flow = Flow(start=think)
flow.run({"question": "PocketFlow 和 LangChain 有什么区别？"})
```

### 4.3 智能体 设计最佳实践

构建高性能 智能体 时，以下原则至关重要：

**上下文管理**：向 LLM 提供**相关且精简**的上下文，而非全量信息。LLM 在处理过长文本时容易"迷失在中间"（lost in the middle），应该用 RAG 检索相关片段而非直接塞入完整历史。

**动作空间设计**：每个 action 应**结构清晰、含义明确**，避免语义重叠。例如，不要同时定义 `search_database` 和 `query_csv` —— 应该合并为统一的 `search_data(source, query)` 接口。

**渐进式信息展示**：不要一次性展示全部信息。先给 LLM 概览（目录、摘要），让它选择要深入的部分。每次最多输入约 500 行内容。

**参数化动作**：让 action 通过参数灵活化。例如 `search_data(query="...", source="db")` 比固定的 `search_database` 和 `search_csv` 更灵活通用。

**错误恢复**：支持**回退**操作，让 智能体 能撤销失败的步骤。部分回退比完全重启更高效。

::: tip 学习要点
- **智能体 核心模式**：Think → Act → Observe 的循环
- **自主决策**：LLM 在 `exec()` 中判断是否需要更多信息
- **工具调用**：`SearchNode.exec()` 调用外部搜索 API
:::


## 5. 多智能体协作

::: info 难度：中级 | 模式：AsyncNode + 消息队列 + 并发 | 关键词：异步通信、协作博弈
:::

### 5.1 场景

Taboo 猜词游戏：一个 智能体 描述词语（不能说出关键词），另一个 智能体 猜词。两个 智能体 通过**异步消息队列**通信，使用 `asyncio.gather()` **并发运行**。

### 5.2 架构

<div align="center"><img src="/easy-pocket/multi-agent.png" width="420"/></div>

*多智能体协作：多个智能体通过发布/订阅模式通信*

两个智能体各自运行独立的 AsyncFlow，通过异步消息队列交换信息，由 `asyncio.gather()` 并发驱动。

### 5.3 核心代码

两个智能体各自继承 `AsyncNode`，使用 `async/await` 三阶段。注意 `prep_async` 中通过 `await queue.get()` 等待对方消息，`post_async` 中通过 `await queue.put()` 发送消息：

```python
import asyncio
from pocketflow import AsyncNode, AsyncFlow

class Hinter智能体(AsyncNode):
    """提示者：描述目标词，不能使用禁忌词"""
    async def prep_async(self, shared):
        msg = await shared["hinter_queue"].get()  # 等待消息
        return {
            "msg": msg,
            "word": shared["word"],
            "taboo_words": shared["taboo_words"],
        }

    async def exec_async(self, data):
        if data["msg"] == "start":
            prompt = f"请描述'{data['word']}'，不能使用：{data['taboo_words']}"
        else:
            prompt = f"对方猜的是'{data['msg']}'，不对。换个方式描述'{data['word']}'，不能使用：{data['taboo_words']}"
        return await async_call_llm(prompt)

    async def post_async(self, shared, prep_res, exec_res):
        await shared["guesser_queue"].put(exec_res)  # 发送提示给猜测者
        if shared.get("game_over"):
            return "end"
        return "continue"

class Guesser智能体(AsyncNode):
    """猜测者：根据提示猜词"""
    async def prep_async(self, shared):
        hint = await shared["guesser_queue"].get()  # 等待提示
        return hint

    async def exec_async(self, hint):
        prompt = f"根据以下描述猜一个词：{hint}"
        return await async_call_llm(prompt)

    async def post_async(self, shared, prep_res, exec_res):
        if exec_res.strip() == shared["word"]:
            shared["game_over"] = True
            print(f"猜对了！答案是「{shared['word']}」")
            return "end"
        shared["round"] = shared.get("round", 0) + 1
        if shared["round"] >= 5:
            shared["game_over"] = True
            print(f"超过 5 轮，游戏结束。答案是「{shared['word']}」")
            return "end"
        await shared["hinter_queue"].put(exec_res)  # 告诉提示者猜错了
        return "continue"

# 每个 智能体 自循环
hinter = Hinter智能体()
hinter - "continue" >> hinter
hinter_flow = AsyncFlow(start=hinter)

guesser = Guesser智能体()
guesser - "continue" >> guesser
guesser_flow = AsyncFlow(start=guesser)

# 两个 智能体 并发运行
async def main():
    shared = {
        "word": "大熊猫",
        "taboo_words": ["熊猫", "国宝", "黑白"],
        "hinter_queue": asyncio.Queue(),
        "guesser_queue": asyncio.Queue(),
    }
    shared["hinter_queue"].put_nowait("start")  # 启动信号

    await asyncio.gather(
        hinter_flow.run_async(shared),
        guesser_flow.run_async(shared),
    )

asyncio.run(main())
```

::: tip 学习要点
- **AsyncNode**：使用 `prep_async` / `exec_async` / `post_async` 异步三阶段
- **消息队列**：`asyncio.Queue` 实现 智能体 间的异步通信
- **并发执行**：`asyncio.gather()` 让两个 智能体 同时运行，通过队列协调
- **自循环**：`agent - "continue" >> agent` 实现 智能体 的持续运行循环
- **AsyncFlow**：AsyncNode **必须**包裹在 AsyncFlow 中，不能用普通 Flow
:::

### 延伸思考：监督者模式（Supervisor）

<div align="center"><img src="/easy-pocket/supervisor.png" width="420"/></div>

*监督者模式：增加审批节点监督子智能体输出*

在多智能体协作的基础上，还有一种常见架构 —— **监督者模式**。它在多个子智能体之外增加一个"监督节点"，负责审批或拒绝子智能体的输出。如果输出不合格，监督节点将任务打回给子智能体重做；如果通过审批，则流程继续推进。这种模式适用于对输出质量要求较高的场景，例如代码审查、多轮校对等。你可以尝试在本案例的基础上，增加一个 `SupervisorNode` 来实现这一架构。
