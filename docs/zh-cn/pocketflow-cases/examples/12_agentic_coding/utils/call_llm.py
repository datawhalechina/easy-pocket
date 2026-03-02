"""
LLM 调用工具

默认使用模拟实现，方便无 API 密钥时直接运行。
如需接入真实 LLM，取消注释下方的 OpenAI 实现即可。
"""

import os


def call_llm(prompt: str) -> str:
    """调用 LLM API（当前为模拟实现）"""
    # ---------- 模拟实现 ----------
    if "SEARCH" in prompt.upper() or "搜索" in prompt:
        if "已有信息" in prompt and len(prompt) > 200:
            return "ANSWER"
        return "SEARCH PocketFlow 设计模式"
    if "ANSWER" in prompt.upper() or "回答" in prompt:
        return "PocketFlow 是一个 100 行代码的极简 LLM 框架，支持多种设计模式。"
    return f"模拟回复：{prompt[:50]}..."

    # ---------- 真实 OpenAI 实现（取消注释即可使用） ----------
    # from openai import OpenAI
    #
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    # r = client.chat.completions.create(
    #     model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return r.choices[0].message.content


if __name__ == "__main__":
    print(call_llm("用一句话解释 PocketFlow"))
