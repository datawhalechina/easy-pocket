"""
案例 10：MCP 工具集成
对应教程：第 10 节 —— MCP 工具集成

模式：智能体 + 工具调用
演示：
- PlanNode：分析任务，制定计划
- SelectTool：根据任务选择合适的 MCP 工具
- ExecuteTool：通过模拟的 MCP 协议执行工具
- ReflectNode：反思执行结果，决定是否继续

MCP (Model Context Protocol) 是一种标准化的工具调用协议。
本示例模拟 MCP 工具调用过程。

注意：本示例使用模拟工具，无需真实 MCP 服务。
入门推荐：https://datawhalechina.github.io/mcp-lite-dev
"""

from pocketflow import Node, Flow


# ========== 模拟 MCP 工具 ==========

_MCP_TOOLS = {
    "calculator": {
        "name": "calculator",
        "description": "数学计算工具，支持四则运算",
        "params": {"expression": "str"},
    },
    "weather": {
        "name": "weather",
        "description": "天气查询工具",
        "params": {"city": "str"},
    },
    "translator": {
        "name": "translator",
        "description": "文本翻译工具",
        "params": {"text": "str", "target_lang": "str"},
    },
}


def get_mcp_tools() -> list[dict]:
    """获取可用的 MCP 工具列表"""
    return list(_MCP_TOOLS.values())


def mcp_execute(tool_name: str, params: dict) -> str:
    """模拟 MCP 工具执行"""
    if tool_name == "calculator":
        expr = params.get("expression", "1+1")
        try:
            result = eval(expr)  # 仅用于演示，生产环境请使用安全的表达式解析
            return f"计算结果：{expr} = {result}"
        except Exception:
            return f"计算错误：无法计算 {expr}"
    elif tool_name == "weather":
        city = params.get("city", "北京")
        return f"{city}天气：晴，25°C，湿度 45%"
    elif tool_name == "translator":
        text = params.get("text", "")
        lang = params.get("target_lang", "en")
        return f"翻译结果 ({lang}): Translation of '{text}'"
    return f"未知工具：{tool_name}"


# ========== 模拟 LLM ==========

_step = 0


def mock_call_llm(prompt: str) -> str:
    """模拟 LLM 决策"""
    global _step
    _step += 1

    if "制定计划" in prompt or "计划" in prompt:
        return "计划：1) 查询北京天气 2) 计算温度转换为华氏度 3) 翻译天气信息为英文"
    elif "选择" in prompt or "工具" in prompt:
        if _step <= 3:
            return "weather"
        elif _step <= 5:
            return "calculator"
        return "translator"
    elif "反思" in prompt or "评估" in prompt:
        if _step <= 6:
            return "continue"
        return "done"
    return "模拟回复"


# ========== 节点定义 ==========

class PlanNode(Node):
    def prep(self, shared):
        return shared["task"]

    def exec(self, task):
        prompt = f"任务：{task}\n请制定计划。"
        plan = mock_call_llm(prompt)
        print(f"[Plan] {plan}")
        return plan

    def post(self, shared, prep_res, exec_res):
        shared["plan"] = exec_res
        shared["execution_log"] = []


class SelectTool(Node):
    def prep(self, shared):
        return {
            "task": shared["task"],
            "plan": shared["plan"],
            "log": shared["execution_log"],
        }

    def exec(self, data):
        available = get_mcp_tools()
        tool_names = [t["name"] for t in available]
        prompt = f"任务：{data['task']}\n可用工具：{tool_names}\n已完成：{data['log']}\n请选择下一个工具。"
        selected = mock_call_llm(prompt)
        print(f"[SelectTool] 选择工具：{selected}")
        return selected

    def post(self, shared, prep_res, exec_res):
        shared["selected_tool"] = exec_res


class ExecuteTool(Node):
    def prep(self, shared):
        return shared["selected_tool"]

    def exec(self, tool_name):
        # 根据工具名称构造参数（模拟）
        params_map = {
            "weather": {"city": "北京"},
            "calculator": {"expression": "25 * 9 / 5 + 32"},
            "translator": {"text": "北京天气晴朗，25度", "target_lang": "en"},
        }
        params = params_map.get(tool_name, {})
        result = mcp_execute(tool_name, params)
        print(f"[ExecuteTool] {tool_name}({params}) → {result}")
        return result

    def post(self, shared, prep_res, exec_res):
        shared["execution_log"].append({
            "tool": shared["selected_tool"],
            "result": exec_res,
        })


class ReflectNode(Node):
    def prep(self, shared):
        return {
            "task": shared["task"],
            "log": shared["execution_log"],
        }

    def exec(self, data):
        prompt = f"任务：{data['task']}\n执行记录：{data['log']}\n请反思和评估：任务是否完成？"
        decision = mock_call_llm(prompt)
        print(f"[Reflect] 决策：{decision}")
        return decision

    def post(self, shared, prep_res, exec_res):
        if "done" in exec_res.lower():
            return "done"
        return "continue"


class OutputNode(Node):
    def prep(self, shared):
        return shared["execution_log"]

    def exec(self, log):
        print(f"\n[Output] 任务完成！执行了 {len(log)} 个工具调用：")
        for i, entry in enumerate(log):
            print(f"  {i + 1}. {entry['tool']} → {entry['result']}")
        return log


# ========== 构建 Flow ==========

if __name__ == "__main__":
    plan = PlanNode()
    select = SelectTool()
    execute = ExecuteTool()
    reflect = ReflectNode()
    output = OutputNode()

    plan >> select >> execute >> reflect
    reflect - "continue" >> select   # 还需要更多工具
    reflect - "done" >> output       # 任务完成

    flow = Flow(start=plan)

    print("=== MCP 工具集成示例 ===\n")
    shared = {"task": "查询北京天气，转换为华氏度，并翻译成英文"}
    flow.run(shared)
