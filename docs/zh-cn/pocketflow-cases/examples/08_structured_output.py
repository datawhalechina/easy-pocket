"""
案例 08：结构化输出 (Structured Output)
对应教程：第 8 节 —— 结构化输出

模式：循环 + 重试 + 校验
演示：
- 让 LLM 生成 JSON 格式输出
- 解析并校验格式（字段、类型、范围）
- 格式不对时自动重新生成
- 双层重试：节点内解析重试 + Flow 层生成重试

注意：本示例使用模拟 LLM，无需 API 密钥。
"""

import json
import re
from pocketflow import Node, Flow


# ========== 模拟 LLM ==========

_call_count = 0


def mock_call_llm(prompt: str) -> str:
    """模拟 LLM 输出，前几次故意输出格式不对"""
    global _call_count
    _call_count += 1

    if _call_count == 1:
        # 第一次：输出非 JSON 格式
        return "张三的 Python 能力不错，我给 85 分。原因是他有丰富的项目经验。"

    if _call_count == 2:
        # 第二次：输出 JSON 但缺少字段
        return '{"name": "张三", "score": 85}'

    # 第三次及以后：输出正确格式
    return '{"name": "张三", "score": 85, "reason": "具备扎实的 Python 基础，有多个开源项目经验"}'


# ========== 节点定义 ==========

class GenerateJSON(Node):
    def prep(self, shared):
        return shared["task"]

    def exec(self, task):
        prompt = f"""请为以下任务生成严格的 JSON 格式结果：
{task}

输出格式：{{"name": "...", "score": 0-100, "reason": "..."}}
只输出 JSON，不要其他文字。"""
        result = mock_call_llm(prompt)
        print(f"  [Generate] LLM 输出：{result[:80]}...")
        return result

    def post(self, shared, prep_res, exec_res):
        shared["raw_output"] = exec_res


class ValidateJSON(Node):
    """解析并校验 JSON 格式"""

    def prep(self, shared):
        return shared["raw_output"]

    def exec(self, raw):
        # 尝试提取 JSON
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            raise ValueError("输出中未找到 JSON")

        data = json.loads(match.group())

        # 校验必需字段
        assert "name" in data, "缺少 name 字段"
        assert "score" in data, "缺少 score 字段"
        assert "reason" in data, "缺少 reason 字段"

        # 校验类型和范围
        assert isinstance(data["score"], (int, float)), "score 必须是数字"
        assert 0 <= data["score"] <= 100, "score 必须在 0-100 之间"

        print(f"  [Validate] 解析成功：{data}")
        return data

    def exec_fallback(self, prep_res, exc):
        print(f"  [Validate] 解析失败：{exc}")
        return None


class CheckResult(Node):
    def prep(self, shared):
        return None

    def exec(self, _):
        return None

    def post(self, shared, prep_res, exec_res):
        # 从 validate 传递结果
        # ValidateJSON 的 post 没有显式定义，exec_res 通过 shared 传递
        # 这里通过检查 shared 中的 result 判断
        result = shared.get("result")
        if result is None:
            shared["retry_count"] = shared.get("retry_count", 0) + 1
            print(f"  [Check] 第 {shared['retry_count']} 次重试...")
            if shared["retry_count"] >= 3:
                print("  [Check] 超过最大重试次数，放弃")
                return "give_up"
            return "retry"
        print(f"  [Check] 结果有效，流程结束")
        return "done"


class ValidateAndStore(Node):
    """合并 Validate 和存储逻辑"""

    def prep(self, shared):
        return shared["raw_output"]

    def exec(self, raw):
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            raise ValueError("输出中未找到 JSON")

        data = json.loads(match.group())

        required = ["name", "score", "reason"]
        for field in required:
            assert field in data, f"缺少 {field} 字段"

        assert isinstance(data["score"], (int, float)), "score 必须是数字"
        assert 0 <= data["score"] <= 100, "score 必须在 0-100 之间"

        print(f"  [Validate] 解析成功：{json.dumps(data, ensure_ascii=False)}")
        return data

    def exec_fallback(self, prep_res, exc):
        print(f"  [Validate] 解析失败：{exc}")
        return None

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        if exec_res is None:
            shared["retry_count"] = shared.get("retry_count", 0) + 1
            print(f"  [Check] 第 {shared['retry_count']} 次重试...")
            if shared["retry_count"] >= 5:
                print("  [Check] 超过最大重试次数，放弃")
                return "give_up"
            return "retry"
        print(f"  [Check] 结果有效")
        return "done"


class OutputNode(Node):
    def prep(self, shared):
        return shared.get("result")

    def exec(self, result):
        if result:
            print(f"\n[最终结果] {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print("\n[最终结果] 未能获取有效的结构化输出")
        return result


# ========== 构建 Flow ==========

if __name__ == "__main__":
    print("=== 结构化输出示例 ===\n")

    generate = GenerateJSON()
    validate = ValidateAndStore(max_retries=2)  # 节点内解析可重试 2 次
    output = OutputNode()

    generate >> validate
    validate - "retry" >> generate     # 格式不对，重新生成
    validate - "done" >> output        # 格式正确，输出
    validate - "give_up" >> output     # 多次失败，放弃

    flow = Flow(start=generate)

    shared = {"task": "评估候选人张三的 Python 编程能力"}
    print(f"任务：{shared['task']}\n")
    flow.run(shared)
