"""
案例 05：多 Agent 协作 (Taboo 猜词游戏)
对应教程：第 5 节 —— 多 Agent 协作

模式：AsyncNode + 消息队列 + 并发
演示：
- HinterAgent：描述目标词（不能说禁忌词）
- GuesserAgent：根据描述猜词
- 两个 Agent 通过 asyncio.Queue 异步通信
- 使用 asyncio.gather() 并发运行

注意：本示例使用模拟 LLM，无需 API 密钥。
"""

import asyncio
from pocketflow import AsyncNode, AsyncFlow


# ========== 模拟异步 LLM ==========

async def mock_hinter_llm(word: str, taboo_words: list, msg: str, round_num: int) -> str:
    """模拟提示者，随着轮次给出更多提示"""
    await asyncio.sleep(0.1)  # 模拟网络延迟
    descriptions = {
        "大熊猫": [
            "这是一种黑白相间的可爱动物，生活在中国的山区，喜欢吃竹子。",
            "它是中国的国宝，圆滚滚的身体，黑色的眼圈是它最显著的特征。",
            "它属于熊科动物，是世界自然基金会(WWF)的标志形象。",
        ],
    }
    descs = descriptions.get(word, [f"这是一个和 '{word}' 相关的东西（第 {round_num} 轮提示）"])
    idx = min(round_num, len(descs) - 1)
    return descs[idx]


async def mock_guesser_llm(hint: str, round_num: int) -> str:
    """模拟猜测者，逐渐接近正确答案"""
    await asyncio.sleep(0.1)  # 模拟网络延迟
    guesses = ["北极熊", "考拉", "大熊猫"]
    idx = min(round_num, len(guesses) - 1)
    return guesses[idx]


# ========== Agent 节点定义 ==========

class HinterAgent(AsyncNode):
    """提示者 Agent：描述目标词，不能使用禁忌词"""

    async def prep_async(self, shared):
        msg = await shared["hinter_queue"].get()  # 等待来自 guesser 的消息
        return {
            "msg": msg,
            "word": shared["word"],
            "taboo_words": shared["taboo_words"],
            "round": shared.get("round", 0),
        }

    async def exec_async(self, data):
        description = await mock_hinter_llm(
            data["word"], data["taboo_words"], data["msg"], data["round"]
        )
        print(f"  [提示者] {description}")
        return description

    async def post_async(self, shared, prep_res, exec_res):
        await shared["guesser_queue"].put(exec_res)  # 发送提示给猜测者
        if shared.get("game_over"):
            return "end"
        return "continue"


class GuesserAgent(AsyncNode):
    """猜测者 Agent：根据提示猜词"""

    async def prep_async(self, shared):
        hint = await shared["guesser_queue"].get()  # 等待来自 hinter 的提示
        return {
            "hint": hint,
            "round": shared.get("round", 0),
        }

    async def exec_async(self, data):
        guess = await mock_guesser_llm(data["hint"], data["round"])
        print(f"  [猜测者] 我猜是：{guess}")
        return guess

    async def post_async(self, shared, prep_res, exec_res):
        if exec_res == shared["word"]:
            shared["game_over"] = True
            print(f"\n  猜对了！答案是「{shared['word']}」")
            return "end"

        shared["round"] = shared.get("round", 0) + 1
        if shared["round"] >= 5:
            shared["game_over"] = True
            print(f"\n  超过 5 轮，游戏结束。答案是「{shared['word']}」")
            return "end"

        print(f"  不对，进入第 {shared['round'] + 1} 轮...\n")
        await shared["hinter_queue"].put(exec_res)  # 告诉提示者猜错了
        return "continue"


# ========== 构建 Flow 并运行 ==========

async def main():
    # 每个 Agent 自循环
    hinter = HinterAgent()
    hinter - "continue" >> hinter
    hinter_flow = AsyncFlow(start=hinter)

    guesser = GuesserAgent()
    guesser - "continue" >> guesser
    guesser_flow = AsyncFlow(start=guesser)

    # 初始化共享状态
    shared = {
        "word": "大熊猫",
        "taboo_words": ["熊猫", "国宝", "黑白"],
        "hinter_queue": asyncio.Queue(),
        "guesser_queue": asyncio.Queue(),
    }

    print("=== Taboo 猜词游戏 (异步多 Agent) ===\n")
    print(f"目标词：{shared['word']}（禁忌词：{shared['taboo_words']}）\n")

    # 发送启动信号
    shared["hinter_queue"].put_nowait("start")

    # 两个 Agent 并发运行
    await asyncio.gather(
        hinter_flow.run_async(shared),
        guesser_flow.run_async(shared),
    )

    rounds = shared.get("round", 0) + 1
    result = "猜对了" if shared.get("game_over") and shared.get("round", 0) < 5 else "未猜出"
    print(f"\n[游戏结束] 共 {rounds} 轮，结果：{result}")


if __name__ == "__main__":
    asyncio.run(main())
