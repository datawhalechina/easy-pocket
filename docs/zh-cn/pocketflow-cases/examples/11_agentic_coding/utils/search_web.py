"""
网页搜索工具

默认使用模拟实现，方便无 API 密钥时直接运行。
如需接入真实搜索 API，替换 search_web 函数体即可。
"""


def search_web(query: str) -> list[str]:
    """搜索网页（当前为模拟实现）"""
    # ---------- 模拟实现 ----------
    mock_db = {
        "PocketFlow": [
            "PocketFlow 是一个 100 行代码的极简 LLM 框架",
            "支持 Node、Flow、BatchNode、AsyncNode 等核心抽象",
        ],
        "设计模式": [
            "六大设计模式：链式调用、条件分支、循环重试、嵌套子流程、批量处理、并行执行",
        ],
    }
    results = []
    for key, values in mock_db.items():
        if key.lower() in query.lower():
            results.extend(values)
    return results or [f"未找到关于 '{query}' 的结果"]

    # ---------- 真实搜索实现（替换为你的搜索 API） ----------
    # import requests
    #
    # url = "https://api.example.com/search"
    # r = requests.get(url, params={"q": query}, timeout=10)
    # r.raise_for_status()
    # data = r.json()
    # return [item["snippet"] for item in data.get("items", [])]


if __name__ == "__main__":
    print(search_web("PocketFlow 设计模式"))
