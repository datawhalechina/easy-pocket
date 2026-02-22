"""
案例 03：RAG 检索增强生成
对应教程：第 3 节 —— RAG 检索增强生成

模式：链式 + BatchNode
演示：
- 离线阶段：Chunk → Embed(BatchNode) → Index
- 在线阶段：Retrieve → Generate
- BatchNode 批量计算 embedding

注意：本示例使用模拟的 embedding 和 LLM，无需 API 密钥。
"""

import math
from pocketflow import Node, BatchNode, Flow


# ========== 模拟工具函数 ==========

def split_text(text: str, chunk_size: int = 50) -> list[str]:
    """简单按字数切分文本"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def mock_compute_embedding(text: str) -> list[float]:
    """模拟 embedding 计算：基于字符哈希生成简单向量"""
    vec = [0.0] * 8
    for i, ch in enumerate(text):
        vec[i % 8] += ord(ch) * 0.001
    # 归一化
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na * nb > 0 else 0.0


def mock_call_llm(prompt: str) -> str:
    """模拟 LLM 回答"""
    if "回答" in prompt or "Answer" in prompt:
        return "基于检索到的上下文，PocketFlow 是一个 100 行代码的极简 LLM 框架，核心只有 Node 和 Flow 两个概念。"
    return "这是一个模拟的 LLM 回复。"


# ========== 离线阶段：构建索引 ==========

class ChunkNode(Node):
    def prep(self, shared):
        return shared["documents"]

    def exec(self, docs):
        chunks = []
        for doc in docs:
            chunks.extend(split_text(doc, chunk_size=50))
        print(f"[Chunk] 切分为 {len(chunks)} 个片段")
        return chunks

    def post(self, shared, prep_res, exec_res):
        shared["chunks"] = exec_res


class EmbedBatch(BatchNode):
    """使用 BatchNode 批量处理每个 chunk"""

    def prep(self, shared):
        return shared["chunks"]  # 返回列表

    def exec(self, chunk):
        # 每个 chunk 独立计算 embedding
        embedding = mock_compute_embedding(chunk)
        return embedding

    def post(self, shared, prep_res, exec_res):
        shared["embeddings"] = exec_res  # 所有 embedding 的列表
        print(f"[Embed] 批量计算完成，共 {len(exec_res)} 个向量")


class IndexNode(Node):
    def prep(self, shared):
        return {
            "chunks": shared["chunks"],
            "embeddings": shared["embeddings"],
        }

    def exec(self, data):
        # 构建简单的内存索引（实际场景用向量数据库）
        index = list(zip(data["chunks"], data["embeddings"]))
        print(f"[Index] 索引构建完成，共 {len(index)} 条记录")
        return index

    def post(self, shared, prep_res, exec_res):
        shared["index"] = exec_res


# ========== 在线阶段：检索回答 ==========

class RetrieveNode(Node):
    def prep(self, shared):
        return {
            "question": shared["question"],
            "index": shared["index"],
        }

    def exec(self, data):
        q_embedding = mock_compute_embedding(data["question"])
        # 计算相似度并排序
        scored = [
            (chunk, cosine_similarity(q_embedding, emb))
            for chunk, emb in data["index"]
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_k = [chunk for chunk, score in scored[:3]]
        print(f"[Retrieve] 检索到 top-3 片段：")
        for i, chunk in enumerate(top_k):
            print(f"  {i + 1}. {chunk[:40]}...")
        return top_k

    def post(self, shared, prep_res, exec_res):
        shared["context"] = "\n".join(exec_res)


class GenerateNode(Node):
    def prep(self, shared):
        return {
            "context": shared["context"],
            "question": shared["question"],
        }

    def exec(self, data):
        prompt = f"基于以下信息回答问题：\n{data['context']}\n\n问题：{data['question']}"
        answer = mock_call_llm(prompt)
        return answer

    def post(self, shared, prep_res, exec_res):
        shared["answer"] = exec_res
        print(f"\n[Generate] 最终回答：{exec_res}")


# ========== 构建并运行 ==========

if __name__ == "__main__":
    # 模拟知识库文档
    documents = [
        "PocketFlow 是一个仅 100 行代码的极简 LLM 应用框架。它零依赖、无厂商锁定。",
        "PocketFlow 的核心只有两个概念：Node（节点）和 Flow（流程）。Node 负责做事，Flow 负责调度。",
        "每个 Node 遵循三阶段模型：prep 从 shared 读取数据，exec 执行核心逻辑，post 将结果写回 shared。",
        "PocketFlow 还提供 BatchNode 用于批量处理，AsyncNode 用于异步并发，支持多种设计模式。",
    ]

    # --- 离线阶段：构建索引 ---
    print("=== 离线阶段：构建索引 ===\n")
    chunk = ChunkNode()
    embed = EmbedBatch()
    index = IndexNode()
    chunk >> embed >> index
    offline_flow = Flow(start=chunk)
    shared = {"documents": documents}
    offline_flow.run(shared)

    # --- 在线阶段：检索回答 ---
    print("\n=== 在线阶段：检索回答 ===\n")
    shared["question"] = "PocketFlow 的核心概念是什么？"
    retrieve = RetrieveNode()
    generate = GenerateNode()
    retrieve >> generate
    online_flow = Flow(start=retrieve)
    online_flow.run(shared)
