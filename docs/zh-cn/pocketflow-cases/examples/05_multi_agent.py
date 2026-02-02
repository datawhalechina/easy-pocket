"""
案例 05：多 Agent 协作 (Taboo 猜词游戏)
对应教程：第 5 节 —— 多 Agent 协作

模式：多 Agent + 循环
演示：
- Describer：描述目标词（不能说禁忌词）
- Guesser：根据描述猜词
- Judge：判断是否猜对，决定继续或结束

注意：本示例使用模拟 LLM，无需 API 密钥。
"""

import random
from pocketflow import Node, Flow


# ========== 模拟 LLM ==========

def mock_describer_llm(word: str, taboo_words: list, round_num: int) -> str:
    """模拟描述者，随着轮次给出更多提示"""
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


def mock_guesser_llm(description: str, round_num: int) -> str:
    """模拟猜测者，逐渐接近正确答案"""
    guesses = ["北极熊", "考拉", "大熊猫"]
    idx = min(round_num, len(guesses) - 1)
    return guesses[idx]


# ========== 节点定义 ==========

class Describer(Node):
    def prep(self, shared):
        return {
            "word": shared["word"],
            "taboo_words": shared["taboo_words"],
            "round": shared.get("round", 0),
        }

    def exec(self, data):
        description = mock_describer_llm(
            data["word"], data["taboo_words"], data["round"]
        )
        print(f"  [描述者] {description}")
        return description

    def post(self, shared, prep_res, exec_res):
        shared["description"] = exec_res


class Guesser(Node):
    def prep(self, shared):
        return {
            "description": shared["description"],
            "round": shared.get("round", 0),
        }

    def exec(self, data):
        guess = mock_guesser_llm(data["description"], data["round"])
        print(f"  [猜测者] 我猜是：{guess}")
        return guess

    def post(self, shared, prep_res, exec_res):
        shared["guess"] = exec_res


class Judge(Node):
    def prep(self, shared):
        return {
            "guess": shared["guess"],
            "word": shared["word"],
            "round": shared.get("round", 0),
        }

    def exec(self, data):
        is_correct = data["guess"] == data["word"]
        print(f"  [裁判] {'正确！' if is_correct else '不对，再试试！'}")
        return is_correct

    def post(self, shared, prep_res, exec_res):
        if exec_res:
            print(f"\n  猜对了！答案是「{shared['word']}」")
            return "correct"

        shared["round"] = shared.get("round", 0) + 1
        if shared["round"] >= 5:
            print(f"\n  超过 5 轮，游戏结束。答案是「{shared['word']}」")
            return "give_up"

        print(f"  进入第 {shared['round'] + 1} 轮...\n")
        return "wrong"


class DoneNode(Node):
    def prep(self, shared):
        return shared

    def exec(self, data):
        rounds = data.get("round", 0) + 1
        result = "猜对了" if data.get("guess") == data["word"] else "未猜出"
        print(f"\n[游戏结束] 共 {rounds} 轮，结果：{result}")
        return result


# ========== 构建 Flow ==========

if __name__ == "__main__":
    describer = Describer()
    guesser = Guesser()
    judge = Judge()
    done = DoneNode()

    describer >> guesser >> judge
    judge - "wrong" >> describer      # 猜错了，再来
    judge - "correct" >> done         # 猜对了
    judge - "give_up" >> done         # 放弃

    flow = Flow(start=describer)

    print("=== Taboo 猜词游戏 ===\n")
    shared = {
        "word": "大熊猫",
        "taboo_words": ["熊猫", "国宝", "黑白"],
    }
    print(f"目标词：{shared['word']}（禁忌词：{shared['taboo_words']}）\n")
    flow.run(shared)
