---
title: 'PocketFlow 应用案例 —— 从入门到进阶的实战全景'
description: '通过 9 个实战案例，学习如何用 PocketFlow 构建聊天机器人、RAG、Agent、工作流、批处理等 LLM 应用。'
---

# PocketFlow 应用案例 (Application Cases)

> **学习指南**：本章精选了 PocketFlow 的 9 个应用案例，从入门到进阶，覆盖聊天、RAG、Agent、批处理、并行等常见模式。每个案例都包含 Flow 架构图、核心代码和学习要点。

<CaseShowcase />

---

## 0. 案例地图：选择你的学习路径

不同背景的读者可以选择不同的入门路径：

<el-tabs type="border-card">
  <el-tab-pane label="零基础入门">

**推荐顺序**：聊天机器人 → 写作工作流 → RAG

这三个案例覆盖了 PocketFlow 的核心模式：链式调用、循环、条件分支。掌握它们，你就能构建大多数 LLM 应用。

  </el-tab-pane>
  <el-tab-pane label="想做 Agent">

**推荐顺序**：搜索 Agent → 多 Agent 协作 → MCP 工具集成 → 智能体编程

Agent 的核心是"自主决策循环"。这四个案例从简单的工具调用，到多 Agent 协作，再到标准化工具集成，最后学习系统化构建 Agent 的工程方法论。

  </el-tab-pane>
  <el-tab-pane label="关注性能">

**推荐顺序**：Map-Reduce 批处理 → 并行图片处理

BatchNode 和 AsyncParallelBatchNode 是 PocketFlow 处理性能问题的核心工具。这两个案例展示如何用简洁的代码获得数倍加速。

  </el-tab-pane>
</el-tabs>

---

## 1. 聊天机器人 (ChatBot)

::: info 难度：入门 | 模式：链式 + 循环 | 关键词：对话历史、多轮对话
:::

### 1.1 架构

```
GetInput → CallLLM → SendReply
    ↑                     |
    └─── "continue" ──────┘
```

### 1.2 核心思路

聊天机器人是最基础的 LLM 应用，它的 Flow 只有三个节点：

1. **GetInput**：从用户获取输入，将其追加到 `shared["history"]`
2. **CallLLM**：拼接对话历史为 prompt，调用 LLM API
3. **SendReply**：输出回复，`post()` 返回 `"continue"` 跳回 GetInput

### 1.3 关键代码

```python
from pocketflow import Node, Flow

class GetInput(Node):
    def prep(self, shared):
        return shared.get("history", [])

    def exec(self, history):
        user_input = input("You: ")
        return user_input

    def post(self, shared, prep_res, exec_res):
        if exec_res.lower() == "quit":
            return "end"
        shared.setdefault("history", []).append(
            {"role": "user", "content": exec_res}
        )
        return "default"

class CallLLM(Node):
    def prep(self, shared):
        return shared["history"]

    def exec(self, history):
        # 调用你的 LLM API
        response = call_llm_api(history)
        return response

    def post(self, shared, prep_res, exec_res):
        shared["history"].append(
            {"role": "assistant", "content": exec_res}
        )
        shared["last_reply"] = exec_res

class SendReply(Node):
    def prep(self, shared):
        return shared["last_reply"]

    def exec(self, reply):
        print(f"AI: {reply}")
        return reply

    def post(self, shared, prep_res, exec_res):
        return "continue"

# 构建 Flow
get_input = GetInput()
call_llm = CallLLM()
send_reply = SendReply()

get_input >> call_llm >> send_reply
send_reply - "continue" >> get_input
get_input - "end" >> None  # 退出

flow = Flow(start=get_input)
flow.run({})
```

::: tip 学习要点
- **循环模式**：`send_reply - "continue" >> get_input` 实现多轮对话
- **shared 通信**：对话历史存在 `shared["history"]` 中
- **退出条件**：`get_input` 的 `post()` 返回 `"end"` 时无后继节点，Flow 结束
:::

---

## 2. RAG 检索增强生成

::: info 难度：入门 | 模式：链式 + BatchNode | 关键词：向量检索、知识库
:::

### 2.1 架构

```
离线索引：Chunk → Embed → Index
在线查询：Retrieve → Generate
```

### 2.2 核心思路

RAG 分两个阶段：

**离线阶段**（构建索引）：
1. **Chunk**：将文档切分成小片段
2. **Embed**：使用 BatchNode 批量计算向量
3. **Index**：存入向量数据库

**在线阶段**（回答问题）：
1. **Retrieve**：根据问题检索相关片段
2. **Generate**：将检索到的 context 和 question 拼接，调用 LLM

### 2.3 关键代码

```python
from pocketflow import Node, BatchNode, Flow

class ChunkNode(Node):
    def prep(self, shared):
        return shared["documents"]

    def exec(self, docs):
        # 将文档切分为 chunk
        chunks = []
        for doc in docs:
            chunks.extend(split_text(doc, chunk_size=500))
        return chunks

    def post(self, shared, prep_res, exec_res):
        shared["chunks"] = exec_res

class EmbedBatch(BatchNode):
    """使用 BatchNode 批量处理每个 chunk"""
    def prep(self, shared):
        return shared["chunks"]  # 返回列表

    def exec(self, chunk):
        # 每个 chunk 独立计算 embedding
        return compute_embedding(chunk)

    def post(self, shared, prep_res, exec_res):
        shared["embeddings"] = exec_res  # 所有结果的列表

class RetrieveNode(Node):
    def prep(self, shared):
        return shared["question"]

    def exec(self, question):
        q_embedding = compute_embedding(question)
        # 向量相似度搜索
        top_k = vector_search(q_embedding, k=3)
        return top_k

    def post(self, shared, prep_res, exec_res):
        shared["context"] = "\n".join(exec_res)

class GenerateNode(Node):
    def prep(self, shared):
        return {
            "context": shared["context"],
            "question": shared["question"]
        }

    def exec(self, data):
        prompt = f"""基于以下信息回答问题：
{data['context']}

问题：{data['question']}"""
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res
        print(f"Answer: {exec_res}")
```

::: tip 学习要点
- **BatchNode**：`EmbedBatch` 的 `prep()` 返回列表，`exec()` 对每个 chunk 独立执行
- **两条 Flow**：离线索引和在线查询是独立的 Flow，共享同一个向量数据库
- **Prompt 拼接**：GenerateNode 将检索结果和问题组合成 prompt
:::

---

## 3. 写作工作流 (Writing Workflow)

::: info 难度：入门 | 模式：链式 | 关键词：多步骤生成、内容流水线
:::

### 3.1 架构

```
Outline → WriteDraft → Polish
```

### 3.2 核心代码

```python
class OutlineNode(Node):
    def prep(self, shared):
        return shared["topic"]

    def exec(self, topic):
        prompt = f"为主题'{topic}'列出文章大纲（3-5 个章节）"
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["outline"] = exec_res

class WriteDraftNode(Node):
    def prep(self, shared):
        return shared["outline"]

    def exec(self, outline):
        prompt = f"根据以下大纲撰写完整文章：\n{outline}"
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["draft"] = exec_res

class PolishNode(Node):
    def prep(self, shared):
        return shared["draft"]

    def exec(self, draft):
        prompt = f"润色以下文章，使语言更流畅：\n{draft}"
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["final_article"] = exec_res

outline >> write_draft >> polish
flow = Flow(start=outline)
flow.run({"topic": "PocketFlow 入门指南"})
```

---

## 4. 搜索 Agent

::: info 难度：中级 | 模式：循环 + 条件分支 | 关键词：工具调用、自主决策
:::

### 4.1 架构

```
Think → Search
  ↑        |
  |   "need_more"
  └────────┘
       |
  "enough"
       ↓
  Synthesize
```

### 4.2 核心代码

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
        return call_llm_api(prompt)

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
        return call_llm_api(prompt)

# 构建 Flow
think >> search
search >> think                      # 搜索后回到思考
think - "enough" >> synthesize       # 信息充分则生成
think - "need_more" >> search        # 信息不足则继续搜索
```

::: tip 学习要点
- **Agent 核心模式**：Think → Act → Observe 的循环
- **自主决策**：LLM 在 `exec()` 中判断是否需要更多信息
- **工具调用**：`SearchNode.exec()` 调用外部搜索 API
:::

---

## 5. 多 Agent 协作

::: info 难度：中级 | 模式：多 Agent + 循环 | 关键词：异步通信、角色扮演
:::

### 5.1 场景

Taboo 猜词游戏：一个 Agent 描述词语（不能说出关键词），另一个 Agent 猜词。

### 5.2 核心代码

```python
class Describer(Node):
    def exec(self, data):
        prompt = f"请描述'{data['word']}'，但不能使用这些词：{data['taboo_words']}"
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["description"] = exec_res

class Guesser(Node):
    def exec(self, description):
        prompt = f"根据以下描述猜一个词：{description}"
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["guess"] = exec_res

class Judge(Node):
    def post(self, shared, prep_res, exec_res):
        if shared["guess"].lower() == shared["word"].lower():
            print("猜对了！")
            return "correct"
        shared["round"] = shared.get("round", 0) + 1
        if shared["round"] >= 5:
            return "give_up"
        return "wrong"

describer >> guesser >> judge
judge - "wrong" >> describer     # 猜错了，再来
judge - "correct" >> done_node   # 猜对了
judge - "give_up" >> done_node   # 放弃
```

---

## 6. Map-Reduce 批处理

::: info 难度：入门 | 模式：BatchNode | 关键词：批量评估、数据聚合
:::

```python
class EvalResume(BatchNode):
    """批量评估简历"""
    def prep(self, shared):
        return shared["resumes"]  # 返回简历列表

    def exec(self, resume):
        # 每份简历独立评分
        prompt = f"请为以下简历评分(1-10)：\n{resume}"
        score = call_llm_api(prompt)
        return {"resume": resume, "score": int(score)}

    def post(self, shared, prep_res, exec_res):
        # exec_res 是所有评分结果的列表
        shared["scores"] = sorted(exec_res, key=lambda x: x["score"], reverse=True)
        print(f"Top 3: {shared['scores'][:3]}")
```

::: tip 学习要点
- `prep()` 返回列表 → `exec()` 对每个元素独立执行 → `post()` 收到结果列表
- 每个元素的 `exec()` 都有独立的重试机制
- 代码量与处理单个元素几乎完全相同
:::

---

## 7. 并行处理 (8x 加速)

::: info 难度：中级 | 模式：AsyncParallelBatchNode | 关键词：并发、I/O 密集
:::

```python
import asyncio
from pocketflow import AsyncParallelBatchNode, AsyncFlow

class ParallelProcess(AsyncParallelBatchNode):
    def prep(self, shared):
        return shared["items"]

    async def exec_async(self, item):
        # 每个 item 并发执行
        result = await async_api_call(item)
        return result

    def post(self, shared, prep_res, exec_res):
        shared["results"] = exec_res

# asyncio.gather() 自动并发所有 item
# I/O 密集场景下可获得 N 倍加速
```

---

## 8. 思维链推理 (Chain-of-Thought)

::: info 难度：进阶 | 模式：循环 + 自检 | 关键词：推理、验证
:::

```python
class StepReason(Node):
    def exec(self, data):
        prompt = f"""问题：{data['question']}
当前推理步骤：{data['steps']}
请继续推理下一步，输出格式：
STEP: [推理过程]
ANSWER: [如果得出答案]"""
        return call_llm_api(prompt)

class Verify(Node):
    def exec(self, data):
        prompt = f"请验证以下推理过程是否正确：\n{data}"
        return call_llm_api(prompt)

    def post(self, shared, prep_res, exec_res):
        if "错误" in exec_res:
            return "error"   # 重新推理
        return "ok"          # 验证通过

step_reason >> verify
verify - "error" >> step_reason  # 发现错误，重推
verify - "ok" >> conclude        # 验证通过，输出
```

---

## 9. MCP 工具集成

::: info 难度：进阶 | 模式：Agent + 工具 | 关键词：MCP 协议、扩展能力
:::

Model Context Protocol (MCP) 是一种标准化的工具调用协议。PocketFlow 通过 Node 的 `exec()` 方法自然地集成 MCP 工具：

> **入门推荐**：[MCP Lite Dev 教程](https://datawhalechina.github.io/mcp-lite-dev) 提供了详细的 MCP 协议学习指南和最佳实践。

```python
class SelectTool(Node):
    def exec(self, data):
        available_tools = get_mcp_tools()  # 获取可用工具列表
        prompt = f"任务：{data['task']}\n可用工具：{available_tools}\n请选择合适的工具。"
        return call_llm_api(prompt)

class ExecuteTool(Node):
    def exec(self, tool_call):
        # 通过 MCP 协议调用工具
        return mcp_execute(tool_call)

plan >> select_tool >> execute_tool >> reflect
reflect - "continue" >> plan      # 需要更多工具
reflect - "done" >> output        # 任务完成
```

---

## 10. 智能体编程 (Agentic Coding)

::: info 难度：进阶 | 模式：人类设计 + 代理实现 | 关键词：系统设计、数据契约、可靠性
:::

智能体编程是一种高效协作范式：**人类负责系统设计，AI 负责实现**。PocketFlow 的核心抽象（Node / Flow / Shared Store）让这种协作更自然。

::: warning 重要提醒
如果你正在用 AI 构建 LLM 系统，请务必牢记三件事：
1) 从**小而简单**的方案开始；2) **先写高层设计文档**（例如 `docs/design.md`）再写代码；3) 频繁向人类确认与复盘。
:::

> **官方指南**：[Agentic Coding: Humans Design, Agents Code](https://the-pocket.github.io/PocketFlow/guide.html#agentic-coding-humans-design-agents-code)

### 10.1 分工原则（谁负责什么）

| 步骤 | 人类参与度 | AI 参与度 | 关键目标 |
| --- | --- | --- | --- |
| 1. 需求澄清 | 高 | 低 | 明确用户问题与价值边界 |
| 2. Flow 设计 | 中 | 中 | 用节点描述高层流程 |
| 3. Utilities | 中 | 中 | 列出外部能力/接口 |
| 4. Data 设计 | 低 | 高 | 设计 shared 数据契约 |
| 5. Node 设计 | 低 | 高 | 明确每个节点读写 |
| 6. 实现 | 低 | 高 | 让 Agent 写代码 |
| 7. 优化 | 中 | 中 | 调整拆分与提示词 |
| 8. 可靠性 | 低 | 高 | 补测试、补校验 |

### 10.2 8 步流程（写在设计文档里）

1. **Requirements**：明确需求，判断是否适合用 AI 解决
   - **适合**：重复性、规则清晰的任务（填表、邮件回复）
   - **适合**：输入明确的创作任务（生成文案、写 SQL）
   - **不适合**：高度模糊且需复杂决策的问题（商业战略、公司治理）
   - **以用户为中心**：先写“用户问题”，再写“功能清单”
   - **复杂度与价值平衡**：优先交付高价值、低复杂度能力

2. **Flow**：用节点描述系统如何协作
   - 识别设计模式：
     - [Map Reduce](https://the-pocket.github.io/PocketFlow/design_pattern/mapreduce.html)
     - [Agent](https://the-pocket.github.io/PocketFlow/design_pattern/agent.html)
     - [RAG](https://the-pocket.github.io/PocketFlow/design_pattern/rag.html)
   - 每个节点写一句话职责
   - 如果是 Map-Reduce：说明“拆分”和“聚合”
   - 如果是 Agent：说明“上下文”和“行动空间”
   - 如果是 RAG：说明“离线索引”和“在线检索”
   - 画流程图（示例）：

   ```mermaid
   flowchart LR
       start[Start] --> batch[Batch]
       batch --> check[Check]
       check -->|OK| process
       check -->|Error| fix[Fix]
       fix --> check

       subgraph process[Process]
         step1[Step 1] --> step2[Step 2]
       end

       process --> endNode[End]
   ```

   ::: tip
   如果人类无法画出 Flow，AI 就无法自动化。建议先手动解几条样例，建立直觉。
   :::

3. **Utilities**：识别并实现外部工具（系统的“身体”）
   - 读取输入：拉取消息、读文件、查数据库
   - 写入输出：发送通知、生成报告
   - 调用外部工具：搜索、API、数据库、LLM
   - **注意**：LLM 内部任务（总结、分析）不是 Utility

   <div align="center"><img src="https://github.com/the-pocket/.github/raw/main/assets/utility.png?raw=true" width="420"/></div>

   - 为每个 Utility 写一个小测试并记录输入输出
   - 示例记录：
     - `name`: `get_embedding` (`utils/get_embedding.py`)
     - `input`: `str`
     - `output`: 3072 维向量
     - `necessity`: 第二个节点需要 embedding

4. **Data**：设计 shared 数据契约
   - 小系统用内存字典；大系统可接数据库
   - **避免重复**：引用或外键优先

   ```python
   shared = {
       "user": {
           "id": "user123",
           "context": {
               "weather": {"temp": 72, "condition": "sunny"},
               "location": "San Francisco"
           }
       },
       "results": {}
   }
   ```

5. **Node**：写清每个节点读写与工具依赖
   - `type`：Regular / Batch / Async
   - `prep`：读 shared 的什么字段
   - `exec`：调用哪个 Utility（不写异常处理）
   - `post`：写回 shared 的什么字段

6. **Implementation**：开始让 Agent 写代码
   - **Keep it simple**：不要一上来就追求复杂特性
   - **Fail fast**：用 Node 的重试/回退机制快速暴露薄弱环节
   - 添加足够日志，方便调试

7. **Optimization**：再迭代
   - 先用直觉做快评估
   - 回到步骤 3–6 重新拆分与优化
   - 提示词更清晰、加入示例减少歧义

8. **Reliability**：补齐稳定性
   - `exec` 内增加结果校验
   - 适当提升 `max_retries` 和 `wait`
   - 加入“自评估节点”对结果做二次检查

   <div align="center"><img src="https://github.com/the-pocket/.github/raw/main/assets/success.png?raw=true" width="420"/></div>

### 10.3 最小设计文档模板（节选）

~~~markdown
# Design Doc: 项目名

## Requirements
- 用户要解决的具体问题：
- 成功标准：

## Flow Design
- 节点列表与一句话说明

```mermaid
flowchart TD
  A[Node A] --> B[Node B]
  B --> C[Node C]
```

## Utilities
- call_llm(prompt: str) -> str
- search_web(query: str) -> list

## Data (shared)
shared = {
  "input": ...,  # 原始输入
  "context": ...,
  "answer": ...
}

## Node Design
- Node A: prep 读 input，exec 调用工具，post 写 context
- Node B: ...
~~~

### 10.4 示例工程结构

```
my_project/
├── main.py
├── nodes.py
├── flow.py
├── utils/
│   ├── __init__.py
│   ├── call_llm.py
│   └── search_web.py
├── requirements.txt
└── docs/
     └── design.md
```

### 10.5 Utilities 实战代码（可直接运行）

```python
# utils/call_llm.py
import os
from openai import OpenAI

def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    r = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

if __name__ == "__main__":
    print(call_llm("用一句话解释 PocketFlow"))
```

```python
# utils/search_web.py
import requests

def search_web(query: str) -> list[str]:
    # 伪实现：请替换为你的搜索 API
    url = "https://api.example.com/search"
    r = requests.get(url, params={"q": query}, timeout=10)
    r.raise_for_status()
    data = r.json()
    return [item["snippet"] for item in data.get("items", [])]

if __name__ == "__main__":
    print(search_web("PocketFlow agentic coding"))
```

### 10.6 Node/Flow/Main 实战代码

```python
# nodes.py
from pocketflow import Node
from utils.call_llm import call_llm
from utils.search_web import search_web

class DecideAction(Node):
    def prep(self, shared):
        return shared["question"], shared.get("context", [])

    def exec(self, data):
        question, context = data
        prompt = f"""问题：{question}
已有信息：{context}
请决定下一步：SEARCH 或 ANSWER。"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        if "SEARCH" in exec_res:
            return "search"
        return "answer"

class Search(Node):
    def prep(self, shared):
        return shared["question"]

    def exec(self, question):
        return search_web(question)

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("context", []).extend(exec_res)

class Answer(Node):
    def prep(self, shared):
        return shared["question"], shared.get("context", [])

    def exec(self, data):
        question, context = data
        prompt = f"""请基于以下信息回答问题：
{context}

问题：{question}"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res
```

```python
# flow.py
from pocketflow import Flow
from nodes import DecideAction, Search, Answer

def create_agent_flow():
    decide = DecideAction()
    search = Search()
    answer = Answer()

    decide - "search" >> search
    decide - "answer" >> answer
    search >> decide  # 搜索后回到判断

    return Flow(start=decide)
```

```python
# main.py
from flow import create_agent_flow

def main():
    shared = {"question": "PocketFlow 有哪些设计模式？"}
    flow = create_agent_flow()
    flow.run(shared)
    print("Answer:", shared.get("answer"))

if __name__ == "__main__":
    main()
```

### 10.7 可靠性增强（重试 + 回退）

```python
from pocketflow import Node
from utils.call_llm import call_llm

class SafeAnswer(Node):
    def exec(self, question):
        if not question:
            raise ValueError("empty question")
        return call_llm(question)

    def exec_fallback(self, prep_res, exc):
        return "抱歉，当前无法生成答案，请稍后再试。"

safe_answer = SafeAnswer(max_retries=3, wait=2)
```

### 10.8 最小可运行测试

```python
# tests/test_nodes.py
from nodes import DecideAction

def test_decide_action_returns_string():
    node = DecideAction()
    shared = {"question": "What is PocketFlow?"}
    action = node.run(shared)
    assert action in ["search", "answer", "default"]
```

::: tip 学习要点
- 智能体编程的核心不是“让 AI 写代码”，而是**让 AI 严格按设计实现**
- 设计文档越清晰，Flow 的可维护性与稳定性越高
- 可靠性靠“检查 + 重试 + 评估节点”来补齐
:::

---

## 配套示例代码

本教程的所有案例都已整理为**完整可运行的 Python 脚本**，存放在 [`examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-cases/examples) 文件夹中。

### 环境配置

::: code-group

```bash [Windows]
python -m venv .venv
.venv\Scripts\activate
cd examples
pip install -r requirements.txt
```

```bash [macOS / Linux]
python -m venv .venv
source .venv/bin/activate
cd examples
pip install -r requirements.txt
```

:::

### 示例一览

| 文件 | 案例 | 核心模式 |
| :--- | :--- | :--- |
| `01_chatbot.py` | 聊天机器人 | 链式 + 循环 |
| `02_rag.py` | RAG 检索增强 | 链式 + BatchNode |
| `03_writing_workflow.py` | 写作工作流 | 链式 |
| `04_search_agent.py` | 搜索 Agent | 循环 + 条件分支 |
| `05_multi_agent.py` | 多 Agent 协作 | 多 Agent + 循环 |
| `06_map_reduce.py` | Map-Reduce | BatchNode |
| `07_parallel_processing.py` | 并行处理 | AsyncParallelBatchNode |
| `08_chain_of_thought.py` | 思维链推理 | 循环 + 自检 |
| `09_mcp_tool.py` | MCP 工具集成 | Agent + 工具 |
| `10_agentic_coding/` | 智能体编程 | 完整项目模板 |

::: code-group

```bash [按学习路径运行]
# 零基础入门
python 01_chatbot.py
python 03_writing_workflow.py
python 02_rag.py

# Agent 方向
python 04_search_agent.py
python 05_multi_agent.py
python 09_mcp_tool.py
cd 10_agentic_coding && python main.py
```

```bash [运行单个示例]
python 04_search_agent.py
```

:::

::: info 关于示例代码
- 所有示例默认使用**模拟 LLM**，无需 API 密钥，开箱即用
- 如需接入真实 LLM，只需替换各文件中的 `mock_` 函数即可
- 案例 10 是完整的多文件项目模板，包含 utils / nodes / flow / tests
:::

---

## 总结

<el-card shadow="hover" style="border-radius: 16px; border: 2px dashed var(--vp-c-brand); margin: 20px 0;">
  <div style="text-align: center;">
    <div style="font-size: 1.25rem; font-weight: 600; color: var(--vp-c-text-1);">
      100 行代码，覆盖主流场景
    </div>
    <div style="color: var(--vp-c-text-3); margin-top: 0.5rem;">
      Node 做事，Flow 调度，shared 通信 —— 三个概念，构建一切。
    </div>
  </div>
</el-card>

### 下一步

- 进入 [`examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-cases/examples) 文件夹，动手跑通本章的配套代码
- 如果还不熟悉 Node / Flow 等核心概念，回到 [PocketFlow 原理入门](../pocketflow-intro/) 章节查看基础讲解和 [配套示例](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-intro/examples)
- 访问 [PocketFlow GitHub](https://github.com/The-Pocket/PocketFlow) 查看更多示例和完整 cookbook
- 选一个案例，尝试修改 `exec()` 逻辑来适配你自己的场景
