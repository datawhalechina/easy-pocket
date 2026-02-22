"""
案例 12：智能体技能 (技能路由)
对应教程：第 12 节 —— 智能体技能

模式：链式 + 条件分支
演示：
- 把领域知识模块化为 Markdown 技能文件
- 智能体根据用户请求动态选择匹配的技能
- 将技能指令注入 LLM prompt，执行任务

注意：本示例使用模拟 LLM，无需 API 密钥。
"""

import os
from pathlib import Path
from pocketflow import Node, Flow


# ========== 模拟 LLM ==========

def mock_select_skill(task: str, skill_names: list) -> str:
    """模拟 LLM 选择技能：根据关键词匹配"""
    task_lower = task.lower()
    if any(kw in task_lower for kw in ["清单", "checklist", "步骤", "steps", "todo"]):
        return "checklist_writer"
    if any(kw in task_lower for kw in ["摘要", "brief", "总结", "summary", "汇报"]):
        return "executive_brief"
    if any(kw in task_lower for kw in ["评审", "review", "审查", "代码"]):
        return "code_reviewer"
    # 默认返回第一个可用技能
    return skill_names[0] if skill_names else "executive_brief"


def mock_apply_skill(task: str, skill_name: str, skill_content: str) -> str:
    """模拟 LLM 按技能指令执行任务"""
    results = {
        "executive_brief": f"""【执行摘要】

关于：{task}

要点：
• PocketFlow 是一个 100 行代码的极简 LLM 框架
• 核心抽象只有 Node 和 Flow 两个概念
• 零依赖，无厂商锁定

风险与建议：
• 风险：社区生态仍在早期阶段
• 建议：从小型项目开始试点，逐步扩大使用范围""",

        "checklist_writer": f"""【实施清单】

任务：{task}

□ 1. 安装 PocketFlow（pip install pocketflow）
□ 2. 创建项目目录结构（nodes.py / flow.py / utils/）
□ 3. 编写设计文档（docs/design.md）
□ 4. 实现工具函数（utils/call_llm.py 等）
□ 5. 实现各 Node 的 prep/exec/post 三阶段
□ 6. 连接 Flow 图（>> 和 - "action" >> 语法）
□ 7. 编写测试用例
□ 8. 运行并验证

完成标准：所有节点可独立测试，Flow 端到端运行无错误""",

        "code_reviewer": f"""【代码评审报告】

评审对象：{task}

✅ 优点：
• 节点职责单一，prep/exec/post 分离清晰
• shared 数据契约明确，便于协作

⚠️ 建议改进：
• exec() 中缺少输入校验，建议添加 assert
• 建议为关键节点设置 max_retries 和 exec_fallback
• 日志不足，建议在 post() 中添加调试输出

总评：代码结构良好，补齐校验和重试后可上线"""
    }
    return results.get(skill_name, f"[{skill_name}] 已处理任务：{task}")


# ========== 工具函数 ==========

def load_skills(skills_dir: str) -> dict:
    """从指定目录加载所有 .md 技能文件"""
    skills = {}
    skills_path = Path(skills_dir)
    if skills_path.exists():
        for md_file in sorted(skills_path.glob("*.md")):
            skills[md_file.stem] = md_file.read_text(encoding="utf-8")
    return skills


# ========== 内置技能（当目录不存在时使用） ==========

BUILTIN_SKILLS = {
    "executive_brief": """# 执行摘要技能
你正在为高管撰写摘要。
## 规则
- 保持简洁，面向决策
- 以 3 个要点开头
- 包含风险和建议的下一步行动
- 避免实现细节""",

    "checklist_writer": """# 清单编写技能
将请求转换为清晰、可执行的清单。
## 规则
- 使用编号步骤
- 每步简短且可验证
- 标注依赖和阻塞项
- 以"完成标准"结尾""",

    "code_reviewer": """# 代码评审技能
对代码进行专业评审。
## 规则
- 分别列出优点和改进建议
- 关注可读性、健壮性、性能
- 给出具体的修改建议
- 以总评结尾"""
}


# ========== 节点定义 ==========

class SelectSkill(Node):
    """根据用户任务选择最匹配的技能"""

    def prep(self, shared):
        # 尝试从目录加载，否则使用内置技能
        skills_dir = shared.get("skills_dir", "./skills")
        skills = load_skills(skills_dir)
        if not skills:
            skills = BUILTIN_SKILLS
            print("  [Skills] 使用内置技能库")
        else:
            print(f"  [Skills] 从 {skills_dir} 加载了 {len(skills)} 个技能")
        return {
            "task": shared["task"],
            "skills": skills,
        }

    def exec(self, data):
        skill_names = list(data["skills"].keys())
        print(f"  [Select] 可用技能：{skill_names}")
        selected = mock_select_skill(data["task"], skill_names)
        print(f"  [Select] 选择技能：{selected}")
        return selected, data["skills"].get(selected, "")

    def post(self, shared, prep_res, exec_res):
        skill_name, skill_content = exec_res
        shared["selected_skill"] = skill_name
        shared["skill_content"] = skill_content


class ApplySkill(Node):
    """将选中的技能注入 prompt 并执行任务"""

    def prep(self, shared):
        return {
            "task": shared["task"],
            "skill_name": shared["selected_skill"],
            "skill_content": shared["skill_content"],
        }

    def exec(self, data):
        # 真实场景中，这里会构造 prompt 并调用 LLM：
        # prompt = f"技能指令：\n{data['skill_content']}\n\n用户任务：\n{data['task']}"
        # return call_llm(prompt)
        result = mock_apply_skill(data["task"], data["skill_name"], data["skill_content"])
        return result

    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res


# ========== 构建 Flow 并运行 ==========

if __name__ == "__main__":
    print("=== 智能体技能示例 ===\n")

    select = SelectSkill()
    apply = ApplySkill()
    select >> apply

    flow = Flow(start=select)

    # 示例 1：执行摘要
    print("--- 任务 1：请总结 PocketFlow 的核心优势 ---\n")
    shared1 = {"task": "请总结 PocketFlow 的核心优势，给技术 VP 汇报用"}
    flow.run(shared1)
    print(f"\n{shared1['result']}\n")

    # 示例 2：实施清单
    print("\n--- 任务 2：搭建一个 PocketFlow 项目的步骤清单 ---\n")
    shared2 = {"task": "搭建一个 PocketFlow 项目的步骤清单"}
    flow.run(shared2)
    print(f"\n{shared2['result']}\n")

    # 示例 3：代码评审
    print("\n--- 任务 3：评审这段 Node 代码的质量 ---\n")
    shared3 = {"task": "评审这段 Node 代码的质量"}
    flow.run(shared3)
    print(f"\n{shared3['result']}")
