---
title: '输出质量：结构化输出、思维链推理'
description: '结构化输出（循环+重试+校验）和思维链推理（循环+自检）的实战案例。'
---

# 输出质量

## 8. 结构化输出（Structured Output）

::: info 难度：中级 | 模式：循环 + 重试 + 校验 | 关键词：JSON 解析、格式验证、可靠输出
:::

### 8.1 架构

通过"生成 → 校验 → 提取"三步循环，确保 LLM 输出符合预期的 JSON 格式：

<div align="center"><img src="/structured-output.png" width="420"/></div>

*结构化输出：生成 → 解析校验 → 提取输出，校验失败则重试*

### 8.2 核心思路

LLM 的输出是自由文本，但下游系统往往需要**结构化数据**（JSON、表格、特定格式）。核心挑战是：LLM 可能输出格式不对的内容。解决方案：**生成 → 解析校验 → 不对就重来**。

### 8.3 关键代码

实现分为三步：GenerateJSON 生成、ValidateJSON 解析校验（带 `max_retries`）、CheckResult 提取输出或决策重试。注意双层重试机制 —— 节点内重试解析，Flow 层重试生成：

```python
import json
import re
from pocketflow import Node, Flow

class GenerateJSON(Node):
    def prep(self, shared):
        return shared["task"]

    def exec(self, task):
        prompt = f"""请为以下任务生成严格的 JSON 格式结果：
{task}

输出格式：{{"name": "...", "score": 0-100, "reason": "..."}}
只输出 JSON，不要其他文字。"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["raw_output"] = exec_res

class ValidateJSON(Node):
    """解析并校验 JSON 格式，利用 max_retries 自动重试解析"""
    def prep(self, shared):
        return shared["raw_output"]

    def exec(self, raw):
        # 提取 JSON 部分
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            raise ValueError("输出中未找到 JSON")
        data = json.loads(match.group())
        # 校验必需字段和类型
        assert "name" in data, "缺少 name 字段"
        assert "score" in data, "缺少 score 字段"
        assert isinstance(data["score"], (int, float)), "score 必须是数字"
        assert 0 <= data["score"] <= 100, "score 必须在 0-100 之间"
        return data

    def exec_fallback(self, prep_res, exc):
        # 解析失败，返回 None 触发重新生成
        print(f"解析失败：{exc}")
        return None

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res  # 写入解析结果（成功为 dict，失败为 None）

class CheckResult(Node):
    def prep(self, shared):
        return shared.get("result")

    def post(self, shared, prep_res, exec_res):
        if shared.get("result") is None:
            shared["retry_count"] = shared.get("retry_count", 0) + 1
            if shared["retry_count"] >= 3:
                return "give_up"
            return "retry"       # 解析失败，让 LLM 重新生成
        return "done"

# 构建 Flow
generate = GenerateJSON()
validate = ValidateJSON(max_retries=2)  # 解析本身可重试 2 次
check = CheckResult()
output = Node()  # 占位输出节点

generate >> validate >> check
check - "retry" >> generate      # 格式不对，重新生成
check - "done" >> output         # 格式正确，输出结果
check - "give_up" >> output      # 多次失败，放弃

flow = Flow(start=generate)
flow.run({"task": "评估候选人张三的 Python 编程能力"})
```

::: tip 学习要点
- **双层重试**：`ValidateJSON(max_retries=2)` 在节点内重试解析，`check - "retry" >> generate` 在 Flow 层重试生成
- **exec_fallback**：解析失败时不抛异常，而是返回 `None` 让后续节点决策
- **防御性解析**：用正则提取 JSON、逐字段校验，应对 LLM 输出的不确定性
- **退出条件**：设置最大重试次数，避免无限循环
:::


## 9. 思维链推理（Chain-of-Thought）

::: info 难度：进阶 | 模式：循环 + 自检 | 关键词：分步推理、自我验证、复杂问题求解
:::

### 9.1 架构

<div align="center"><img src="/cot.png" width="380"/></div>

*思维链：循环推理 + 思考历史存储*

分步推理 + 自我验证的循环架构 —— 每推一步就校验，错了则回退重推。Verify 有三条出路：步骤有误时 `"error"` 回退重推；步骤正确但未完成时 `"continue"` 继续下一步；全部完成时 `"ok"` 进入 Conclude 输出答案。

### 9.2 核心思路

复杂问题（数学、逻辑、多步规划）直接让 LLM 一步回答容易出错。解决方案：**分步推理，每步验证**。

1. **StepReason**：每次只推理一步，追加到推理链
2. **Verify**：检查最新一步是否正确，不正确则回退重推
3. **Conclude**：推理完成后，整合所有步骤给出最终答案

### 9.3 关键代码

三个节点各司其职：StepReason 推理一步、Verify 校验正确性、Conclude 整合答案。`shared["steps"]` 列表记录完整推理链，验证失败时 `pop()` 回退：

```python
from pocketflow import Node, Flow

class StepReason(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "steps": shared.get("steps", []),
        }

    def exec(self, data):
        prompt = f"""问题：{data['question']}
已有推理步骤：{data['steps']}
请继续推理下一步，输出格式：
STEP: [推理过程]
ANSWER: [如果已得出最终答案]"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("steps", []).append(exec_res)
        shared["latest_step"] = exec_res

class Verify(Node):
    def prep(self, shared):
        return {
            "steps": shared["steps"],
            "latest_step": shared["latest_step"],
        }

    def exec(self, data):
        prompt = f"请验证以下推理是否正确：\n{data['steps']}\n如果有错误请指出。"
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        if "错误" in exec_res:
            shared["steps"].pop()       # 移除错误的步骤
            return "error"              # 回退重推
        if "ANSWER" in shared.get("latest_step", ""):
            return "ok"                 # 已得出答案
        return "continue"               # 正确但未完成

class Conclude(Node):
    def prep(self, shared):
        return shared["steps"]

    def exec(self, steps):
        prompt = f"基于以下推理步骤，给出最终答案：\n{steps}"
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res

# 构建 Flow
step_reason = StepReason()
verify = Verify()
conclude = Conclude()

step_reason >> verify
verify - "error" >> step_reason     # 发现错误，重推
verify - "continue" >> step_reason  # 继续推理下一步
verify - "ok" >> conclude           # 验证通过，输出

flow = Flow(start=step_reason)
flow.run({"question": "一个水池有 A、B 两个进水管，A 管 4 小时注满，B 管 6 小时注满，同时开两管几小时注满？"})
```

::: tip 学习要点
- **分步推理**：每次只推理一步，降低单步出错概率
- **自我验证**：Verify 节点检查推理正确性，错误则回退
- **步骤管理**：`shared["steps"]` 列表记录完整推理链，验证失败时 `pop()` 回退
- **与结构化输出的区别**：结构化输出校验**格式**，思维链校验**逻辑**
:::
