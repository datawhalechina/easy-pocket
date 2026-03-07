---
title: '高级智能体：MCP 工具集成、智能体技能'
description: 'MCP 工具集成（智能体+工具）和智能体技能路由（链式+条件路由）的实战案例。'
---

# 高级智能体

## 10. MCP 工具集成

::: info 难度：进阶 | 模式：智能体 + 工具 | 关键词：MCP 协议、标准化工具调用、扩展能力
:::

### 10.1 架构

智能体在每轮循环中选择工具、执行调用、反思结果，直到任务完成：

```
SelectTool → ExecuteTool → Reflect
    ↑                         │
    └──── "continue" ─────────┘
                              │ "done"
                              ↓
                           Output
```

### 10.2 核心思路

Model Context Protocol (MCP) 是一种标准化的工具调用协议 —— 让 LLM 能以统一的方式调用各种外部工具（搜索、数据库、文件系统等）。PocketFlow 通过 Node 的 `exec()` 方法自然地集成 MCP 工具。

> **入门推荐**：[MCP Lite Dev 教程](https://datawhalechina.github.io/mcp-lite-dev) 提供了详细的 MCP 协议学习指南和最佳实践。

### 10.3 关键代码

三个节点组成典型的智能体循环：SelectTool 让 LLM 选择工具、ExecuteTool 通过 MCP 协议调用、Reflect 判断任务是否完成：

```python
from pocketflow import Node, Flow

class SelectTool(Node):
    """让 LLM 从可用工具中选择最合适的"""
    def prep(self, shared):
        return {
            "task": shared["task"],
            "results": shared.get("results", []),
        }

    def exec(self, data):
        available_tools = get_mcp_tools()  # 获取 MCP 工具列表
        prompt = f"任务：{data['task']}\n已有结果：{data['results']}\n可用工具：{available_tools}\n请选择工具并指定参数。"
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["tool_call"] = exec_res

class ExecuteTool(Node):
    """通过 MCP 协议调用选中的工具"""
    def prep(self, shared):
        return shared["tool_call"]

    def exec(self, tool_call):
        return mcp_execute(tool_call)  # MCP 标准调用

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("results", []).append(exec_res)

class Reflect(Node):
    """判断任务是否完成"""
    def prep(self, shared):
        return {
            "task": shared["task"],
            "results": shared["results"],
        }

    def exec(self, data):
        prompt = f"任务：{data['task']}\n已获得：{data['results']}\n任务完成了吗？输出 DONE 或 CONTINUE。"
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        if "DONE" in exec_res:
            shared["answer"] = exec_res
            return "done"
        return "continue"

# 构建 Flow
select_tool = SelectTool()
execute_tool = ExecuteTool()
reflect = Reflect()
output = Node()  # 占位输出节点

select_tool >> execute_tool >> reflect
reflect - "continue" >> select_tool  # 还需要更多工具
reflect - "done" >> output           # 任务完成

flow = Flow(start=select_tool)
flow.run({"task": "查询北京今天的天气并生成播报文案"})
```

::: tip 学习要点
- **MCP 是协议，不是工具**：它定义了"如何调用工具"的标准，具体有哪些工具由你的 MCP 服务器决定
- **与搜索智能体 的区别**：搜索智能体 只有一个工具（搜索），MCP 智能体 可以选择多种工具
- **Reflect 节点**：智能体 每次使用工具后反思是否已完成任务，避免不必要的额外调用
- **`get_mcp_tools()` 和 `mcp_execute()`**：这两个是你的工具函数（参见[原理篇 §6](../pocketflow-intro/tools-and-dev#_6-工具函数层-node-里装什么)），具体实现取决于你连接的 MCP 服务器
:::

## 11. 智能体技能（技能路由）

::: info 难度：中级 | 模式：链式 + 条件路由 | 关键词：技能文件、动态 Prompt、模块化知识
:::

智能体技能 是一种将**领域知识模块化为独立文件**的模式。智能体 根据用户请求动态选择技能，将技能指令注入 LLM prompt，实现"一个 智能体，多种能力"。

> **核心思路**：技能 = Markdown 文件，选择技能 = 路由节点，执行技能 = Prompt 注入。

### 11.1 问题场景

你有一个通用 智能体，但需要处理多种不同类型的任务 —— 写摘要、列清单、做评审。如果为每种任务写一个独立的 Node 和 Flow，代码会迅速膨胀。

**智能体技能 的解法**：把每种任务的指令写成一个 Markdown 文件（技能），智能体 在运行时根据用户输入**动态选择**并加载。

### 11.2 架构设计

<div align="center"><img src="/easy-pocket/agent-skill.png" width="420"/></div>

*技能路由：选择技能 → 加载指令 → 执行任务*

**两个节点**，职责清晰：
1. **SelectSkill**：列出所有可用技能，根据用户意图选择最匹配的一个
2. **ApplySkill**：读取选中技能的指令，拼入 prompt，调用 LLM 执行

### 11.3 技能文件示例

技能文件就是普通的 Markdown，包含指令和规则：

```markdown
<!-- skills/executive_brief.md -->
# 执行摘要技能
你正在为高管撰写摘要。
## 规则
- 保持简洁，面向决策
- 以 3 个要点开头
- 包含风险和建议的下一步行动
- 避免实现细节
```

另一个技能文件专注于将任务转化为可执行的清单：

```markdown
<!-- skills/checklist_writer.md -->
# 清单编写技能
将请求转换为清晰、可执行的清单。
## 规则
- 使用编号步骤
- 每步简短且可验证
- 标注依赖和阻塞项
- 以"完成标准"结尾
```

### 11.4 核心代码

SelectSkill 扫描技能目录并让 LLM 匹配最合适的技能，ApplySkill 将技能指令注入 prompt 执行任务：

```python
from pathlib import Path
from pocketflow import Node, Flow

def load_skills(skills_dir: str) -> dict:
    """从目录加载所有 .md 技能文件"""
    skills = {}
    for md_file in sorted(Path(skills_dir).glob("*.md")):
        skills[md_file.stem] = md_file.read_text(encoding="utf-8")
    return skills

class SelectSkill(Node):
    """根据用户任务选择最匹配的技能"""
    def prep(self, shared):
        return {
            "task": shared["task"],
            "skills": load_skills(shared.get("skills_dir", "./skills")),
        }

    def exec(self, data):
        skill_names = list(data["skills"].keys())
        # 让 LLM 根据任务描述选择最匹配的技能
        prompt = f"任务：{data['task']}\n可用技能：{skill_names}\n请返回最匹配的技能名。"
        selected = call_llm(prompt)  # 返回技能名字符串
        return selected, data["skills"].get(selected, "")

    def post(self, shared, prep_res, exec_res):
        skill_name, skill_content = exec_res
        shared["selected_skill"] = skill_name
        shared["skill_content"] = skill_content

class ApplySkill(Node):
    """将选中的技能注入 prompt 并执行任务"""
    def prep(self, shared):
        return {
            "task": shared["task"],
            "skill_name": shared["selected_skill"],
            "skill_content": shared["skill_content"],
        }

    def exec(self, data):
        prompt = f"""你正在执行一个智能体技能。
技能名：{data['skill_name']}
技能指令：
---
{data['skill_content']}
---
用户任务：{data['task']}
请严格按照技能指令完成任务。"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res

# 构建 Flow
select = SelectSkill()
apply = ApplySkill()
select >> apply
flow = Flow(start=select)

# 运行
shared = {"task": "总结 PocketFlow 的核心优势，给技术 VP 汇报用"}
flow.run(shared)
print(shared["result"])
```

### 11.5 为什么这个模式有价值？

| 传统做法 | 智能体技能 |
| :--- | :--- |
| 每种任务写一个 Node 类 | 一个通用 Flow，技能文件即插即用 |
| 新增任务 = 改代码 | 新增任务 = 加一个 .md 文件 |
| 指令硬编码在 Python 中 | 指令与代码分离，非开发者也能维护 |
| 测试需要跑整个 Flow | 技能文件可以独立 review 和迭代 |

::: tip 学习要点
- 技能文件是**纯 Markdown**，不是代码 —— 产品经理、运营人员都能编写和维护
- SelectSkill 本身可以用 LLM 做路由（语义匹配），也可以用关键词规则（确定性路由）
- 这个模式可以和 智能体 循环组合：智能体 在每轮决策中选择不同的 Skill 来执行
- 详见 [原理篇 §6：工具函数层](../pocketflow-intro/tools-and-dev#_6-工具函数层-node-里装什么) 了解 PocketFlow 的工具函数体系
:::
