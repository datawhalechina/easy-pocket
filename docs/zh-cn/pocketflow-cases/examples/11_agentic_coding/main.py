"""
主入口

运行搜索 Agent：
  python main.py
"""

from flow import create_agent_flow


def main():
    shared = {"question": "PocketFlow 有哪些设计模式？"}

    print("=== Agentic Coding 示例 ===\n")
    print(f"问题：{shared['question']}\n")

    flow = create_agent_flow(safe_mode=True)
    flow.run(shared)

    print(f"\nAnswer: {shared.get('answer')}")


if __name__ == "__main__":
    main()
