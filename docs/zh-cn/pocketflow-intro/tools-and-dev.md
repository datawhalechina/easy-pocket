---
title: '工具函数与开发范式'
description: 'Node 里装什么？工具函数分类、Agentic Coding 开发范式与名词速查表。'
---

# 6. 工具函数层：Node 里装什么？

前面 5 章讲的都是 PocketFlow **框架本身** —— Node 生命周期、Flow 图遍历、通信机制、设计模式、源码实现。但 PocketFlow 是纯编排框架，**不包含任何具体实现**。那么 Node 的 `exec()` 里到底填什么？

答案是**工具函数**（Utility Functions）—— 你自己编写或引入的外部能力：

| 工具函数类别 | 用途 | 常见选择 |
| :--- | :--- | :--- |
| **LLM 调用** | 文本生成、分析、决策 | OpenAI / Claude / 本地模型 |
| **Web 搜索** | 获取实时信息 | Google / Bing / DuckDuckGo |
| **文本切片** | 将长文档拆成小块 | 按段落 / 按 token 数 / 递归拆分 |
| **Embedding** | 将文本转为向量 | OpenAI / HuggingFace / 本地模型 |
| **向量数据库** | 存储和检索向量 | Pinecone / FAISS / Chroma |

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
- **设计模式**（[§4](./communication-and-patterns#_4-六大设计模式)）= 图拓扑，决定节点之间**怎么连**
- **工具函数**（本节）= 节点内部，决定每个节点**做什么**

两者正交：同一个 LLM 调用工具可以用在链式工作流里，也可以用在 智能体 循环里。PocketFlow 不限制你用什么工具，你可以自由组合。
:::

更进一步，工具函数也可以被**模块化为技能文件**（Markdown），智能体 在运行时动态选择并注入 prompt —— 这就是 **智能体技能** 模式。详见 [应用案例第 11 节：智能体技能](../pocketflow-cases/advanced-agents#_11-智能体技能-技能路由)。


# 7. 开发者体验：Agentic Coding

PocketFlow 推崇一种高效的人机协作开发范式 —— **Agentic Coding**：

> **人类负责设计架构**（定义 Node、画 Flow 图、设计 shared 数据契约），**AI 负责写实现代码**（填充 `exec()` 方法体）。

为什么 PocketFlow 特别适合这种模式？

- **核心极简**：AI 只需理解 Node 和 Flow 两个概念
- **接口清晰**：每个 Node 的输入输出都通过 shared 明确定义
- **零依赖**：不需要理解复杂的第三方 API
- **可测试**：每个 Node 的 `exec()` 可以独立测试

::: info 完整方法论
Agentic Coding 包含 8 个步骤：需求澄清 → Flow 设计 → Utilities 识别 → Data 契约 → Node 设计 → 实现 → 优化 → 可靠性。完整的流程讲解、设计文档模板和可运行示例代码，请参考 [应用案例第 12 节：智能体编程](../pocketflow-cases/agentic-coding#_12-智能体编程-agentic-coding)。
:::

# 8. 名词速查表（Glossary）

| 名词 | 翻译 | 解释 |
| :--- | :--- | :--- |
| Node | 执行的最小单元 | 包含 prep → exec → post 三阶段生命周期。 |
| Flow | 图执行引擎 | 从 start_node 开始，沿 action 遍历有向图。 |
| shared | 全局共享字典 | 节点间通信的主要渠道，所有 Node 都能读写。 |
| params | 局部参数字典 | 由父 Flow 传入，节点通过 `self.params` 读取，适合传递任务标识。 |
| action | 路由标签 | post() 返回的字符串，Flow 据此决定下一个节点。 |
| BatchNode | 批处理节点 | 对列表中每个元素独立执行 exec()。 |
| BatchFlow | 批量流程 | 用不同 params 多次运行整条 Flow。 |
| AsyncNode | 异步节点 | 提供 async/await 版本的三阶段方法，必须在 AsyncFlow 中运行。 |
| AsyncFlow | 异步图引擎 | 支持混合同步/异步节点的异步版 Flow。 |
| prep | 准备阶段 | 从 shared 读取数据，传给 exec。 |
| exec | 执行阶段 | 核心业务逻辑，不直接访问 shared。 |
| post | 后处理阶段 | 将结果写回 shared，返回 action。 |
| exec_fallback | 降级回调 | 所有重试耗尽后调用，可覆写以返回兜底结果。 |

### 下一步

- 前往 [PocketFlow 应用案例](../pocketflow-cases/) 学习实战案例
- 访问 [PocketFlow GitHub](https://github.com/The-Pocket/PocketFlow) 查看完整 cookbook
