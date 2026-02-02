"""
案例 06：Map-Reduce 批处理
对应教程：第 6 节 —— Map-Reduce 批处理

模式：BatchNode
演示：
- 使用 BatchNode 批量评估简历
- prep() 返回简历列表
- exec() 对每份简历独立评分
- post() 收到结果列表并聚合排序

注意：本示例使用模拟评分逻辑，无需 API 密钥。
"""

from pocketflow import BatchNode, Flow


# ========== 模拟 LLM 评分 ==========

def mock_eval_resume(resume: str) -> int:
    """模拟简历评分：基于关键词匹配"""
    score = 5  # 基础分
    keywords = {
        "Python": 1, "LLM": 2, "AI": 1, "机器学习": 1,
        "硕士": 1, "博士": 2, "5年": 1, "10年": 2,
        "架构": 1, "开源": 1, "论文": 1,
    }
    for keyword, points in keywords.items():
        if keyword in resume:
            score += points
    return min(score, 10)


# ========== 节点定义 ==========

class EvalResume(BatchNode):
    """批量评估简历"""

    def prep(self, shared):
        resumes = shared["resumes"]
        print(f"[EvalResume] 准备评估 {len(resumes)} 份简历\n")
        return resumes  # 返回简历列表

    def exec(self, resume):
        # 每份简历独立评分（这里每次只处理一份！）
        score = mock_eval_resume(resume)
        name = resume.split("，")[0] if "，" in resume else resume[:10]
        print(f"  评估：{name}... → {score}/10 分")
        return {"resume": resume, "score": score}

    def post(self, shared, prep_res, exec_res):
        # exec_res 是所有评分结果的列表
        sorted_results = sorted(exec_res, key=lambda x: x["score"], reverse=True)
        shared["scores"] = sorted_results


class ShowResults(BatchNode):
    """展示评估结果"""

    def prep(self, shared):
        return shared["scores"]

    def exec(self, item):
        return item

    def post(self, shared, prep_res, exec_res):
        print(f"\n[结果排名]")
        for i, item in enumerate(shared["scores"]):
            name = item["resume"].split("，")[0]
            print(f"  #{i + 1} {name} — {item['score']}/10 分")
        print(f"\nTop 3 推荐入围面试！")


# ========== 运行 ==========

if __name__ == "__main__":
    resumes = [
        "张三，Python 开发者，5年经验，熟悉 AI 和机器学习",
        "李四，前端工程师，3年经验，擅长 React 和 Vue",
        "王五，AI 研究员，博士学历，发表多篇论文，精通 LLM 和 Python",
        "赵六，全栈工程师，10年经验，有架构设计经验，参与开源项目",
        "陈七，数据分析师，硕士学历，熟悉 Python 和机器学习",
    ]

    eval_node = EvalResume()
    show_node = ShowResults()
    eval_node >> show_node

    flow = Flow(start=eval_node)

    print("=== Map-Reduce 批量简历评估 ===\n")
    shared = {"resumes": resumes}
    flow.run(shared)
