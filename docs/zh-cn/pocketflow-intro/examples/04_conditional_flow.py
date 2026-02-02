"""
示例 04：条件分支
对应教程：第 1.3 节 —— 连接节点的两种方式 & 第 4 节 —— 六大设计模式

演示：
- 使用 - "action" >> target 实现条件分支
- post() 返回不同的 action 字符串，让 Flow 走不同路径
"""

from pocketflow import Node, Flow


class ReviewNode(Node):
    """审核节点：根据分数决定通过或拒绝"""

    def prep(self, shared):
        return shared.get("score", 0)

    def exec(self, score):
        print(f"[Review] 审核分数：{score}")
        if score >= 60:
            return "approve"
        else:
            return "reject"

    def post(self, shared, prep_res, exec_res):
        shared["decision"] = exec_res
        # 返回 action 字符串，Flow 根据它选择下一个节点
        return exec_res


class ApproveNode(Node):
    """通过节点"""

    def exec(self, prep_res):
        print("[Approve] 审核通过！恭喜！")
        return "approved"

    def post(self, shared, prep_res, exec_res):
        shared["result"] = "审核通过"


class RejectNode(Node):
    """拒绝节点"""

    def exec(self, prep_res):
        print("[Reject] 审核未通过，请重试。")
        return "rejected"

    def post(self, shared, prep_res, exec_res):
        shared["result"] = "审核未通过"


if __name__ == "__main__":
    review = ReviewNode()
    approve = ApproveNode()
    reject = RejectNode()

    # 使用条件连接：- "action" >> target
    review - "approve" >> approve
    review - "reject" >> reject

    flow = Flow(start=review)

    # 测试 1：分数 80，应该走 approve 分支
    print("--- 测试 1：分数 80 ---")
    shared1 = {"score": 80}
    flow.run(shared1)
    print(f"结果：{shared1['result']}\n")

    # 测试 2：分数 45，应该走 reject 分支
    print("--- 测试 2：分数 45 ---")
    shared2 = {"score": 45}
    flow.run(shared2)
    print(f"结果：{shared2['result']}")
