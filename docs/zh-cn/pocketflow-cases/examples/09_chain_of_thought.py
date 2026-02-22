"""
案例 09：思维链推理 (Chain-of-Thought)
对应教程：第 9 节 —— 思维链推理

模式：循环 + 自检
演示：
- StepReason：逐步推理
- Verify：验证推理过程
- 发现错误时回到推理节点重做
- 验证通过后输出最终结论

注意：本示例使用模拟推理逻辑，无需 API 密钥。
"""

from pocketflow import Node, Flow


# ========== 模拟 LLM 推理 ==========

def mock_reason(question: str, steps: list) -> str:
    """模拟逐步推理"""
    reasoning_chain = [
        "STEP: 首先，PocketFlow 的核心只有两个抽象：Node 和 Flow。",
        "STEP: Node 遵循 prep → exec → post 三阶段模型，其中 exec 是纯业务逻辑。",
        "STEP: Flow 通过有向图调度 Node，根据 action 决定跳转。",
        "ANSWER: PocketFlow 通过 Node（三阶段执行）和 Flow（图调度）两个核心抽象，"
        "用 100 行代码实现了 LLM 应用的流程编排、状态管理和容错扩展。",
    ]
    idx = min(len(steps), len(reasoning_chain) - 1)
    return reasoning_chain[idx]


def mock_verify(steps: list, latest: str) -> str:
    """模拟验证推理过程"""
    # 模拟：第一个步骤总是正确的，但如果步骤太少，还需继续
    if "ANSWER" in latest:
        return "验证通过：推理过程完整，逻辑自洽。"
    if len(steps) < 2:
        return "验证通过，但推理不完整，请继续推理下一步。"
    return "验证通过：当前推理步骤正确。"


# ========== 节点定义 ==========

class StepReason(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "steps": shared.get("steps", []),
        }

    def exec(self, data):
        result = mock_reason(data["question"], data["steps"])
        print(f"[推理] {result}")
        return result

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("steps", []).append(exec_res)
        shared["latest_step"] = exec_res


class Verify(Node):
    def prep(self, shared):
        return {
            "steps": shared["steps"],
            "latest": shared["latest_step"],
        }

    def exec(self, data):
        verification = mock_verify(data["steps"], data["latest"])
        print(f"[验证] {verification}")
        return verification

    def post(self, shared, prep_res, exec_res):
        if "错误" in exec_res:
            # 发现错误，移除最后一步，重新推理
            shared["steps"].pop()
            print("[验证] 发现错误，回到推理阶段重做\n")
            return "error"

        if "ANSWER" in shared["latest_step"]:
            # 已得出最终答案
            return "ok"

        # 验证通过但还没得出答案，继续推理
        return "continue"


class Conclude(Node):
    def prep(self, shared):
        return shared["steps"]

    def exec(self, steps):
        # 从最后一步提取答案
        answer = steps[-1]
        if "ANSWER:" in answer:
            answer = answer.split("ANSWER:")[1].strip()
        return answer

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res
        print(f"\n[结论] {exec_res}")


# ========== 构建 Flow ==========

if __name__ == "__main__":
    step_reason = StepReason()
    verify = Verify()
    conclude = Conclude()

    step_reason >> verify
    verify - "error" >> step_reason      # 发现错误，重推
    verify - "continue" >> step_reason   # 继续推理下一步
    verify - "ok" >> conclude            # 验证通过，输出

    flow = Flow(start=step_reason)

    print("=== 思维链推理示例 ===\n")
    shared = {"question": "PocketFlow 如何用 100 行代码实现 LLM 应用框架？"}
    print(f"问题：{shared['question']}\n")
    flow.run(shared)

    print(f"\n推理步数：{len(shared['steps'])}")
