"""
示例 06：Node 重试机制
对应教程：第 3.2 节 —— Node 可重试的执行单元

演示：
- 使用 max_retries 和 wait 参数实现自动重试
- exec_fallback 处理所有重试都失败的情况
- 模拟不稳定的 API 调用场景
"""

import random
from pocketflow import Node, Flow


class UnstableApiNode(Node):
    """模拟一个不稳定的 API 调用，有一定概率失败"""

    def prep(self, shared):
        return shared.get("prompt", "Hello")

    def exec(self, prompt):
        # 模拟 60% 概率失败的 API
        if random.random() < 0.6:
            print(f"  [尝试 {self.cur_retry + 1}/{self.max_retries}] API 调用失败！")
            raise ConnectionError("模拟网络错误")

        result = f"API 返回：处理 '{prompt}' 成功"
        print(f"  [尝试 {self.cur_retry + 1}/{self.max_retries}] {result}")
        return result

    def exec_fallback(self, prep_res, exc):
        """所有重试都失败后的兜底逻辑"""
        fallback = f"兜底结果：使用缓存回答 '{prep_res}'"
        print(f"  [兜底] 所有重试均失败，使用 fallback: {fallback}")
        return fallback

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        print(f"  [结果] {exec_res}")


if __name__ == "__main__":
    random.seed(42)  # 固定随机种子以便复现

    # 创建带重试的节点：最多重试 5 次，每次间隔 0.5 秒
    # 实际场景中，调用 LLM API 建议设置 max_retries=3, wait=2
    api_node = UnstableApiNode(max_retries=5, wait=0.5)

    flow = Flow(start=api_node)

    print("=== 运行不稳定 API 示例（max_retries=5, wait=0.5s）===\n")
    shared = {"prompt": "解释量子计算"}
    flow.run(shared)

    print(f"\n最终结果：{shared['result']}")
