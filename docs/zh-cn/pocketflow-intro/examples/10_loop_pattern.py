"""
示例 10：循环/重试模式（自校正）
对应教程：第 4 节 —— 六大设计模式中的"循环/重试"

演示：
- post() 返回的 action 可以指向前序节点，形成循环
- 常用于"生成 → 检查 → 不满意则重做"的自校正模式
"""

from pocketflow import Node, Flow


class GenerateNode(Node):
    """生成节点：模拟 LLM 生成回答"""

    def prep(self, shared):
        attempt = shared.get("attempt", 0) + 1
        shared["attempt"] = attempt
        return {"question": shared["question"], "attempt": attempt}

    def exec(self, data):
        # 模拟随着尝试次数增加，回答质量逐渐提升
        quality_map = {
            1: "PocketFlow 是一个框架。",                            # 太简短
            2: "PocketFlow 是一个 LLM 框架，用于构建应用。",           # 还行
            3: "PocketFlow 是一个仅 100 行代码的极简 LLM 框架，"      # 达标
               "支持 Node 和 Flow 两个核心抽象，零依赖。",
        }
        answer = quality_map.get(data["attempt"], quality_map[3])
        print(f"  [生成] 第 {data['attempt']} 次尝试：{answer}")
        return answer

    def post(self, shared, prep_res, exec_res):
        shared["current_answer"] = exec_res


class CheckNode(Node):
    """检查节点：评估回答质量"""

    def prep(self, shared):
        return shared["current_answer"]

    def exec(self, answer):
        # 简单的质量检查：长度 >= 30 视为合格
        score = len(answer)
        is_good = score >= 30
        print(f"  [检查] 长度 = {score}，{'合格' if is_good else '不合格'}")
        return is_good

    def post(self, shared, prep_res, exec_res):
        if exec_res:
            shared["final_answer"] = shared["current_answer"]
            return "accept"  # 通过，结束循环
        else:
            return "retry"   # 不通过，回到生成节点


class OutputNode(Node):
    """输出节点"""

    def prep(self, shared):
        return shared["final_answer"]

    def exec(self, answer):
        print(f"\n  [输出] 最终回答：{answer}")
        return answer


if __name__ == "__main__":
    generate = GenerateNode()
    check = CheckNode()
    output = OutputNode()

    # 构建循环：生成 → 检查 → (retry) → 生成 / (accept) → 输出
    generate >> check
    check - "retry" >> generate   # 不合格，回到生成节点
    check - "accept" >> output    # 合格，进入输出节点

    flow = Flow(start=generate)

    print("=== 循环/自校正模式示例 ===\n")
    shared = {"question": "什么是 PocketFlow？"}
    flow.run(shared)

    print(f"\n总尝试次数：{shared['attempt']}")
