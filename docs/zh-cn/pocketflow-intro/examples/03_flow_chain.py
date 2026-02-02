"""
示例 03：Flow 链式调用与图执行
对应教程：第 1.2 节 —— Flow 图编排引擎 & 第 1.3 节 —— 连接节点

演示：
- 使用 >> 操作符链式连接多个节点
- Flow 从 start_node 开始，沿 action 遍历有向图
"""

from pocketflow import Node, Flow


class FetchNode(Node):
    """步骤 1：获取用户问题"""

    def prep(self, shared):
        return shared.get("question", "")

    def exec(self, question):
        print(f"[Fetch] 收到问题：{question}")
        return question

    def post(self, shared, prep_res, exec_res):
        shared["question"] = exec_res
        return "default"  # 走默认路径到下一个节点


class ThinkNode(Node):
    """步骤 2：思考并生成回答（模拟）"""

    def prep(self, shared):
        return shared["question"]

    def exec(self, question):
        # 模拟 LLM 生成回答
        answer = f"关于「{question}」，PocketFlow 的回答是：这是一个很好的问题！"
        print(f"[Think] 生成回答：{answer}")
        return answer

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res
        return "default"


class OutputNode(Node):
    """步骤 3：格式化输出"""

    def prep(self, shared):
        return shared["answer"]

    def exec(self, answer):
        formatted = f"=== 回答 ===\n{answer}\n============"
        print(f"[Output] 格式化完成")
        return formatted

    def post(self, shared, prep_res, exec_res):
        shared["formatted_answer"] = exec_res
        print(exec_res)


if __name__ == "__main__":
    # 使用 >> 操作符连接三个节点：Fetch → Think → Output
    fetch = FetchNode()
    think = ThinkNode()
    output = OutputNode()

    fetch >> think >> output

    # 构建 Flow 并运行
    flow = Flow(start=fetch)
    flow.run({"question": "什么是 PocketFlow？"})
