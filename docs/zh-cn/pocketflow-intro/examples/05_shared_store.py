"""
示例 05：Shared 共享存储 —— 节点间通信
对应教程：第 2 节 —— Shared：节点间的通信机制

演示：
- 节点之间通过 shared 字典传递数据
- prep 从 shared 读取，post 向 shared 写入
- 所有节点都能读写同一个 shared 字典
"""

from pocketflow import Node, Flow


class InputNode(Node):
    """输入节点：向 shared 写入初始数据"""

    def exec(self, prep_res):
        print("[Input] 准备用户数据")
        return {"question": "什么是 PocketFlow？", "language": "zh"}

    def post(self, shared, prep_res, exec_res):
        shared["question"] = exec_res["question"]
        shared["language"] = exec_res["language"]
        print(f"[Input] 写入 shared: question='{shared['question']}', language='{shared['language']}'")


class TranslateNode(Node):
    """翻译节点：从 shared 读取，翻译后写回"""

    def prep(self, shared):
        # 从 shared 读取数据
        return {
            "question": shared["question"],
            "language": shared["language"],
        }

    def exec(self, data):
        # 模拟翻译
        if data["language"] == "zh":
            translated = "What is PocketFlow?"
        else:
            translated = data["question"]
        print(f"[Translate] 翻译结果：{translated}")
        return translated

    def post(self, shared, prep_res, exec_res):
        # 写回 shared
        shared["translated_question"] = exec_res
        print(f"[Translate] 写入 shared: translated_question='{exec_res}'")


class AnswerNode(Node):
    """回答节点：读取翻译后的问题，生成回答"""

    def prep(self, shared):
        return shared["translated_question"]

    def exec(self, question):
        answer = f"Answer to '{question}': PocketFlow is a 100-line LLM framework."
        print(f"[Answer] 生成回答：{answer}")
        return answer

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res
        print(f"[Answer] 写入 shared: answer='{exec_res}'")


if __name__ == "__main__":
    input_node = InputNode()
    translate = TranslateNode()
    answer = AnswerNode()

    input_node >> translate >> answer

    flow = Flow(start=input_node)
    shared = {}
    flow.run(shared)

    print("\n--- shared 最终状态 ---")
    for key, value in shared.items():
        print(f"  {key}: {value}")
