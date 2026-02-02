"""
示例 07：嵌套 Flow（子流程）
对应教程：第 3.3 节 —— Flow 图执行引擎

演示：
- Flow 本身也是 BaseNode 的子类
- 子 Flow 可以作为节点参与到父 Flow 中
- 构建分层的复杂流程
"""

from pocketflow import Node, Flow


# ========== 子流程：数据验证 ==========

class ValidateFormatNode(Node):
    """验证数据格式"""

    def prep(self, shared):
        return shared.get("data", "")

    def exec(self, data):
        is_valid = len(data) > 0
        print(f"  [子流程-格式验证] 数据 '{data}' 格式{'有效' if is_valid else '无效'}")
        return is_valid

    def post(self, shared, prep_res, exec_res):
        shared["format_valid"] = exec_res


class ValidateLengthNode(Node):
    """验证数据长度"""

    def prep(self, shared):
        return shared.get("data", "")

    def exec(self, data):
        is_valid = len(data) <= 100
        print(f"  [子流程-长度验证] 长度 {len(data)}，{'通过' if is_valid else '超限'}")
        return is_valid

    def post(self, shared, prep_res, exec_res):
        shared["length_valid"] = exec_res


# ========== 主流程 ==========

class PrepareNode(Node):
    """主流程第 1 步：准备数据"""

    def prep(self, shared):
        return shared.get("raw_input", "")

    def exec(self, raw_input):
        cleaned = raw_input.strip()
        print(f"[主流程-准备] 清洗数据：'{raw_input}' → '{cleaned}'")
        return cleaned

    def post(self, shared, prep_res, exec_res):
        shared["data"] = exec_res


class ProcessNode(Node):
    """主流程第 3 步：处理数据"""

    def prep(self, shared):
        return {
            "data": shared["data"],
            "format_ok": shared.get("format_valid", False),
            "length_ok": shared.get("length_valid", False),
        }

    def exec(self, info):
        if info["format_ok"] and info["length_ok"]:
            result = f"成功处理数据：{info['data']}"
        else:
            result = f"数据验证未通过，跳过处理"
        print(f"[主流程-处理] {result}")
        return result

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        print(f"[主流程-完成] {exec_res}")


if __name__ == "__main__":
    # 构建子流程：格式验证 → 长度验证
    validate_format = ValidateFormatNode()
    validate_length = ValidateLengthNode()
    validate_format >> validate_length
    validation_flow = Flow(start=validate_format)

    # 构建主流程：准备 → [验证子流程] → 处理
    prepare = PrepareNode()
    process = ProcessNode()
    prepare >> validation_flow >> process
    main_flow = Flow(start=prepare)

    # 运行
    print("=== 嵌套 Flow 示例 ===\n")
    shared = {"raw_input": "  PocketFlow 是极简 LLM 框架  "}
    main_flow.run(shared)
