"""
节点单元测试

运行方式：
  cd 10_agentic_coding
  python -m pytest tests/ -v

或者直接运行：
  python tests/test_nodes.py
"""

import sys
import os

# 将父目录加入 path，以便直接运行本文件
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes import DecideAction, Search, Answer, SafeAnswer


def test_decide_action_returns_valid_action():
    """DecideAction 应返回 'search' 或 'answer'"""
    node = DecideAction()
    shared = {"question": "What is PocketFlow?"}
    action = node.run(shared)
    assert action in ["search", "answer", None], f"Unexpected action: {action}"
    print(f"  DecideAction returned: {action}")


def test_search_returns_results():
    """Search 应返回搜索结果列表"""
    node = Search()
    shared = {"question": "PocketFlow", "search_query": "PocketFlow"}
    node.run(shared)
    assert "context" in shared, "Search should populate context"
    assert len(shared["context"]) > 0, "Should have at least one result"
    print(f"  Search returned {len(shared['context'])} results")


def test_answer_generates_response():
    """Answer 应生成回答"""
    node = Answer()
    shared = {
        "question": "What is PocketFlow?",
        "context": ["PocketFlow is a 100-line LLM framework"],
    }
    node.run(shared)
    assert "answer" in shared, "Answer should populate answer"
    assert len(shared["answer"]) > 0, "Answer should not be empty"
    print(f"  Answer: {shared['answer'][:50]}...")


def test_safe_answer_fallback():
    """SafeAnswer 空问题应触发 fallback"""
    node = SafeAnswer(max_retries=2, wait=0)
    shared = {"question": "", "context": []}
    node.run(shared)
    assert "answer" in shared
    assert "抱歉" in shared["answer"], "Should use fallback message"
    print(f"  SafeAnswer fallback: {shared['answer']}")


if __name__ == "__main__":
    tests = [
        test_decide_action_returns_valid_action,
        test_search_returns_results,
        test_answer_generates_response,
        test_safe_answer_fallback,
    ]
    print("=== 运行节点单元测试 ===\n")
    passed = 0
    for test in tests:
        try:
            print(f"运行 {test.__name__}...")
            test()
            print(f"  PASSED\n")
            passed += 1
        except AssertionError as e:
            print(f"  FAILED: {e}\n")
        except Exception as e:
            print(f"  ERROR: {e}\n")

    print(f"结果：{passed}/{len(tests)} 通过")
