"""
示例 02：Node 三阶段生命周期
对应教程：第 1.1 节 —— Node 执行的最小单元

演示 prep → exec → post 三阶段模型：
- prep：从 shared 读取数据
- exec：执行核心业务逻辑（不访问 shared）
- post：将结果写回 shared，返回 action
"""

from pocketflow import Node, Flow


class SummarizeNode(Node):
    """一个模拟"文本摘要"的节点，展示三阶段的职责分离"""

    def prep(self, shared):
        """阶段 1：从 shared 中读取待处理的文本"""
        text = shared.get("text", "")
        print(f"[prep] 从 shared 读取文本，长度 = {len(text)} 字符")
        return text

    def exec(self, text):
        """阶段 2：执行核心逻辑（这里用简单截取模拟摘要）"""
        # 注意：exec 完全不知道 shared 的存在，只处理 prep 传来的数据
        summary = text[:50] + "..." if len(text) > 50 else text
        print(f"[exec] 生成摘要：{summary}")
        return summary

    def post(self, shared, prep_res, exec_res):
        """阶段 3：将结果写回 shared"""
        shared["summary"] = exec_res
        print(f"[post] 摘要已写入 shared['summary']")
        # 不返回 action（默认 None），Flow 将在此节点后结束


if __name__ == "__main__":
    shared = {
        "text": "PocketFlow 是一个仅 100 行代码、零依赖的 LLM 应用框架。"
                "它通过 Node 和 Flow 两个核心抽象，覆盖了 LLM 应用开发中几乎所有的主流模式。"
    }

    node = SummarizeNode()
    flow = Flow(start=node)
    flow.run(shared)

    print(f"\n最终结果：{shared['summary']}")
