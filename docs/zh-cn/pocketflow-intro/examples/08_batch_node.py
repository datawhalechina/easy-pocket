"""
示例 08：BatchNode 批量处理
对应教程：第 3.4 节 —— BatchNode 批量处理

演示：
- prep() 返回一个列表
- exec() 对列表中每个元素独立执行
- 每个元素独享 Node 的重试机制
"""

from pocketflow import BatchNode, Flow


class TranslateBatchNode(BatchNode):
    """批量翻译节点：对多个文本分别执行翻译"""

    def prep(self, shared):
        texts = shared.get("texts", [])
        print(f"[BatchNode] 准备翻译 {len(texts)} 条文本")
        # prep 返回列表，exec 将对每个元素独立调用
        return texts

    def exec(self, text):
        # 这里每次只处理一个文本（不是列表！）
        # 模拟翻译逻辑
        translation = f"[EN] {text} → translated"
        print(f"  翻译：{text} → {translation}")
        return translation

    def post(self, shared, prep_res, exec_res):
        # exec_res 是所有翻译结果的列表
        shared["translations"] = exec_res
        print(f"\n[BatchNode] 完成，共 {len(exec_res)} 条翻译结果")


if __name__ == "__main__":
    texts = [
        "你好世界",
        "PocketFlow 很简单",
        "批量处理真方便",
        "每个元素独立重试",
    ]

    batch_translate = TranslateBatchNode(max_retries=2)
    flow = Flow(start=batch_translate)

    print("=== BatchNode 批量处理示例 ===\n")
    shared = {"texts": texts}
    flow.run(shared)

    print("\n--- 翻译结果 ---")
    for original, translated in zip(texts, shared["translations"]):
        print(f"  {original} → {translated}")
