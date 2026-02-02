"""
示例 01：Hello PocketFlow
对应教程：第 6.2 节 —— 第一个 Flow

演示最基本的 Node + Flow 用法：
- 定义一个 GreetNode，实现 prep / exec / post 三阶段
- 构建单节点 Flow 并运行
"""

from pocketflow import Node, Flow


class GreetNode(Node):
    def prep(self, shared):
        return shared.get("name", "World")

    def exec(self, name):
        return f"Hello, {name}! Welcome to PocketFlow."

    def post(self, shared, prep_res, exec_res):
        shared["greeting"] = exec_res
        print(exec_res)


if __name__ == "__main__":
    # 构建并运行
    greet = GreetNode()
    flow = Flow(start=greet)
    flow.run({"name": "小明"})
    # 输出：Hello, 小明! Welcome to PocketFlow.
