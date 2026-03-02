"""
节点定义

三个核心节点：
- DecideAction：决定下一步是搜索还是回答
- Search：执行搜索
- Answer：生成最终回答
"""

from pocketflow import Node
from utils.call_llm import call_llm
from utils.search_web import search_web


class DecideAction(Node):
    """决策节点：判断是搜索还是直接回答"""

    def prep(self, shared):
        return shared["question"], shared.get("context", [])

    def exec(self, data):
        question, context = data
        prompt = f"""问题：{question}
已有信息：{context}
请决定下一步：SEARCH <关键词> 或 ANSWER。"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        if "SEARCH" in exec_res.upper():
            shared["search_query"] = exec_res.replace("SEARCH", "").strip()
            return "search"
        return "answer"


class Search(Node):
    """搜索节点：执行网页搜索"""

    def prep(self, shared):
        return shared.get("search_query", shared["question"])

    def exec(self, query):
        return search_web(query)

    def post(self, shared, prep_res, exec_res):
        shared.setdefault("context", []).extend(exec_res)


class Answer(Node):
    """回答节点：基于收集的信息生成答案"""

    def prep(self, shared):
        return shared["question"], shared.get("context", [])

    def exec(self, data):
        question, context = data
        prompt = f"""请基于以下信息回答问题：
{context}

问题：{question}"""
        return call_llm(prompt)

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res


class SafeAnswer(Answer):
    """带重试和回退的回答节点"""

    def exec(self, data):
        question, context = data
        if not question:
            raise ValueError("empty question")
        return super().exec(data)

    def exec_fallback(self, prep_res, exc):
        return "抱歉，当前无法生成答案，请稍后再试。"
