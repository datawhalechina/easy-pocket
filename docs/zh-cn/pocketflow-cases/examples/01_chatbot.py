"""
案例 01：聊天机器人 (ChatBot)
对应教程：第 1 节 —— 聊天机器人

模式：链式 + 循环
演示：
- 三个节点组成多轮对话循环：GetInput → CallLLM → SendReply → (循环)
- 对话历史存储在 shared["history"] 中
- 输入 "quit" 退出对话

注意：本示例使用模拟 LLM，无需 API 密钥。
如需接入真实 LLM，替换 mock_call_llm 即可。
"""

from pocketflow import Node, Flow


# ========== 模拟 LLM（替换为真实 API 即可） ==========

def mock_call_llm(history: list) -> str:
    """模拟 LLM 回复，基于简单规则匹配"""
    last_msg = history[-1]["content"] if history else ""
    last_lower = last_msg.lower()

    if "你好" in last_msg or "hello" in last_lower:
        return "你好！我是 PocketFlow 聊天助手，有什么可以帮你的？"
    elif "pocketflow" in last_lower:
        return "PocketFlow 是一个仅 100 行代码的极简 LLM 框架，支持 Node、Flow、BatchNode 等核心抽象。"
    elif "谢谢" in last_msg:
        return "不客气！还有其他问题吗？"
    else:
        return f"你说的是「{last_msg}」，这个话题很有趣！你还想了解什么？"


# ========== 节点定义 ==========

class GetInput(Node):
    def prep(self, shared):
        return shared.get("history", [])

    def exec(self, history):
        user_input = input("You: ")
        return user_input

    def post(self, shared, prep_res, exec_res):
        if exec_res.lower() == "quit":
            return "end"
        shared.setdefault("history", []).append(
            {"role": "user", "content": exec_res}
        )
        return "default"


class CallLLM(Node):
    def prep(self, shared):
        return shared["history"]

    def exec(self, history):
        response = mock_call_llm(history)
        return response

    def post(self, shared, prep_res, exec_res):
        shared["history"].append(
            {"role": "assistant", "content": exec_res}
        )
        shared["last_reply"] = exec_res


class SendReply(Node):
    def prep(self, shared):
        return shared["last_reply"]

    def exec(self, reply):
        print(f"AI: {reply}")
        return reply

    def post(self, shared, prep_res, exec_res):
        return "continue"


# ========== 构建 Flow ==========

if __name__ == "__main__":
    get_input = GetInput()
    call_llm = CallLLM()
    send_reply = SendReply()

    get_input >> call_llm >> send_reply
    send_reply - "continue" >> get_input

    flow = Flow(start=get_input)

    print("=== PocketFlow 聊天机器人 ===")
    print("输入 'quit' 退出对话\n")
    flow.run({})

    print("\n对话结束！")
