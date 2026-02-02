"""
案例 04：搜索 Agent
对应教程：第 4 节 —— 搜索 Agent

模式：循环 + 条件分支
演示：
- Think → Act → Observe 的 Agent 核心循环
- ThinkNode 自主决策是否需要更多搜索
- 条件分支：need_more → 继续搜索 / enough → 生成答案

注意：本示例使用模拟的搜索和 LLM，无需 API 密钥。
"""

from pocketflow import Node, Flow


# ========== 模拟工具函数 ==========

_SEARCH_DB = {
    "PocketFlow 框架": [
        "PocketFlow 是 100 行代码的极简 LLM 框架",
        "支持 Node、Flow、BatchNode 等核心抽象",
    ],
    "PocketFlow 设计模式": [
        "支持六大设计模式：链式调用、条件分支、循环重试、嵌套子流程、批量处理、并行执行",
        "所有模式都是 Node + Flow 的自然组合",
    ],
    "PocketFlow 安装": [
        "pip install pocketflow 即可安装",
        "零依赖，也可以直接复制 100 行源码",
    ],
}


def mock_web_search(query: str) -> list[str]:
    """模拟搜索引擎"""
    results = []
    for key, values in _SEARCH_DB.items():
        if any(word in query for word in key.split()):
            results.extend(values)
    if not results:
        results = [f"未找到关于 '{query}' 的相关结果"]
    return results


_search_count = 0


def mock_call_llm(prompt: str) -> str:
    """模拟 LLM 决策"""
    global _search_count
    if "请决定" in prompt or "决定" in prompt:
        _search_count += 1
        if _search_count <= 2:
            return "PocketFlow 设计模式"  # 继续搜索
        return "ENOUGH"  # 信息够了
    elif "搜索结果回答" in prompt or "基于" in prompt:
        return "PocketFlow 是一个 100 行代码的极简 LLM 框架，支持六大设计模式，通过 pip install pocketflow 安装。"
    return prompt


# ========== 节点定义 ==========

class ThinkNode(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "search_results": shared.get("search_results", []),
        }

    def exec(self, data):
        prompt = f"""问题：{data['question']}
已有信息：{data['search_results']}
请决定：还需要搜索什么？输出搜索关键词，或输出 ENOUGH 表示信息充分。"""
        decision = mock_call_llm(prompt)
        print(f"[Think] 决策：{decision}")
        return decision

    def post(self, shared, prep_res, exec_res):
        if "ENOUGH" in exec_res:
            return "enough"
        shared["search_query"] = exec_res
        return "need_more"


class SearchNode(Node):
    def prep(self, shared):
        return shared["search_query"]

    def exec(self, query):
        results = mock_web_search(query)
        print(f"[Search] 查询 '{query}'，找到 {len(results)} 条结果")
        for r in results:
            print(f"  - {r}")
        return results

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("search_results", []).extend(exec_res)


class SynthesizeNode(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "results": shared["search_results"],
        }

    def exec(self, data):
        prompt = f"基于以下搜索结果回答问题...\n{data}"
        answer = mock_call_llm(prompt)
        print(f"[Synthesize] 最终答案：{answer}")
        return answer

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res


# ========== 构建 Flow ==========

if __name__ == "__main__":
    think = ThinkNode()
    search = SearchNode()
    synthesize = SynthesizeNode()

    think - "need_more" >> search
    think - "enough" >> synthesize
    search >> think  # 搜索后回到思考

    flow = Flow(start=think)

    print("=== 搜索 Agent 示例 ===\n")
    shared = {"question": "PocketFlow 是什么？有哪些设计模式？"}
    flow.run(shared)

    print(f"\n最终答案：{shared['answer']}")
