"""
案例 02：写作工作流 (Writing Workflow)
对应教程：第 2 节 —— 写作工作流

模式：链式
演示：
- 三步写作流水线：大纲 → 初稿 → 润色
- 每个节点调用 LLM 完成一个子任务
- shared 在节点间传递中间结果

注意：本示例使用模拟 LLM，无需 API 密钥。
"""

from pocketflow import Node, Flow


# ========== 模拟 LLM ==========

def mock_call_llm(prompt: str) -> str:
    """模拟 LLM，根据提示词类型返回不同结果"""
    if "大纲" in prompt:
        return (
            "1. PocketFlow 简介\n"
            "   - 什么是 PocketFlow\n"
            "   - 为什么选择 PocketFlow\n"
            "2. 核心概念\n"
            "   - Node：三阶段执行模型\n"
            "   - Flow：图编排引擎\n"
            "3. 实战案例\n"
            "   - 构建一个简单的聊天机器人\n"
            "4. 总结与展望"
        )
    elif "撰写" in prompt or "文章" in prompt:
        return (
            "# PocketFlow 入门指南\n\n"
            "PocketFlow 是一个仅 100 行代码的 LLM 框架。"
            "它的核心理念是极简：只需要 Node 和 Flow 两个概念，"
            "就能构建从聊天机器人到复杂智能体的各种 LLM 应用。\n\n"
            "## 核心概念\n\n"
            "Node 遵循 prep → exec → post 三阶段模型，"
            "Flow 则负责按照有向图的方式调度这些节点。\n\n"
            "## 实战案例\n\n"
            "你只需要几十行代码，就能搭建一个多轮对话机器人。\n\n"
            "## 总结\n\n"
            "PocketFlow 证明了简单即是力量。"
        )
    elif "润色" in prompt:
        return (
            "# PocketFlow 入门指南\n\n"
            "PocketFlow 是一个仅用 100 行代码打造的极简 LLM 应用框架。"
            "它的设计哲学朴素而有力：**只需 Node 和 Flow 两个核心抽象**，"
            "就足以构建从简单的聊天机器人到复杂多智能体系统的各类 LLM 应用。\n\n"
            "## 核心概念\n\n"
            "每个 **Node** 遵循优雅的三阶段模型——prep（准备）、exec（执行）、"
            "post（后处理），而 **Flow** 则以有向图的方式调度这些节点，"
            "让流程编排变得直观而灵活。\n\n"
            "## 实战案例\n\n"
            "只需几十行代码，你就能搭建一个支持多轮对话的智能机器人。\n\n"
            "## 总结\n\n"
            "PocketFlow 用最少的代码，释放了 LLM 最大的潜力。**简单即是力量。**"
        )
    return "模拟 LLM 回复"


# ========== 节点定义 ==========

class OutlineNode(Node):
    def prep(self, shared):
        return shared["topic"]

    def exec(self, topic):
        prompt = f"为主题'{topic}'列出文章大纲（3-5 个章节）"
        outline = mock_call_llm(prompt)
        print(f"[大纲] 生成完成：\n{outline}\n")
        return outline

    def post(self, shared, prep_res, exec_res):
        shared["outline"] = exec_res


class WriteDraftNode(Node):
    def prep(self, shared):
        return shared["outline"]

    def exec(self, outline):
        prompt = f"根据以下大纲撰写完整文章：\n{outline}"
        draft = mock_call_llm(prompt)
        print(f"[初稿] 生成完成（{len(draft)} 字）\n")
        return draft

    def post(self, shared, prep_res, exec_res):
        shared["draft"] = exec_res


class PolishNode(Node):
    def prep(self, shared):
        return shared["draft"]

    def exec(self, draft):
        prompt = f"润色以下文章，使语言更流畅：\n{draft}"
        polished = mock_call_llm(prompt)
        print(f"[润色] 完成（{len(polished)} 字）\n")
        return polished

    def post(self, shared, prep_res, exec_res):
        shared["final_article"] = exec_res


# ========== 构建并运行 ==========

if __name__ == "__main__":
    outline = OutlineNode()
    write_draft = WriteDraftNode()
    polish = PolishNode()

    outline >> write_draft >> polish
    flow = Flow(start=outline)

    print("=== 写作工作流示例 ===\n")
    shared = {"topic": "PocketFlow 入门指南"}
    flow.run(shared)

    print("=" * 50)
    print("最终文章：")
    print("=" * 50)
    print(shared["final_article"])
