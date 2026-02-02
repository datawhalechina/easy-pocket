"""
Flow 定义

构建搜索 Agent 的完整流程图：
DecideAction → Search → DecideAction (循环)
DecideAction → Answer (结束)
"""

from pocketflow import Flow
from nodes import DecideAction, Search, Answer, SafeAnswer


def create_agent_flow(safe_mode: bool = False):
    """创建 Agent Flow

    Args:
        safe_mode: 是否使用带重试的 SafeAnswer 节点
    """
    decide = DecideAction()
    search = Search()
    answer = SafeAnswer(max_retries=3, wait=1) if safe_mode else Answer()

    decide - "search" >> search
    decide - "answer" >> answer
    search >> decide  # 搜索后回到判断

    return Flow(start=decide)
