# PocketFlow 应用案例 —— 配套示例代码

本文件夹包含 [PocketFlow 应用案例教程](../index.md) 中所有代码示例的**完整可运行版本**。

## 环境准备

### 1. Python 版本

需要 **Python 3.9+**（推荐 3.10 或更高版本）。

```bash
python --version
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 示例列表

### 入门案例

| 文件 | 案例 | 核心模式 | 交互方式 |
| :--- | :--- | :--- | :--- |
| `01_chatbot.py` | 聊天机器人 | 链式 + 循环 | 需要终端输入 |
| `02_writing_workflow.py` | 写作工作流 | 链式 | 自动运行 |
| `03_rag.py` | RAG 检索增强 | 链式 + BatchNode | 自动运行 |

### 中级案例

| 文件 | 案例 | 核心模式 | 交互方式 |
| :--- | :--- | :--- | :--- |
| `04_search_agent.py` | 搜索智能体 | 循环 + 条件分支 | 自动运行 |
| `05_multi_agent.py` | 多智能体协作 | 多智能体 + 循环 | 自动运行 |
| `06_map_reduce.py` | Map-Reduce 批处理 | BatchNode | 自动运行 |
| `07_parallel_processing.py` | 并行处理 | AsyncParallelBatchNode | 自动运行 |
| `08_structured_output.py` | 结构化输出 | 循环 + 重试 + 校验 | 自动运行 |
| `11_agent_skills.py` | 智能体技能 | 链式 + 条件路由 | 自动运行 |

### 进阶案例

| 文件 | 案例 | 核心模式 | 交互方式 |
| :--- | :--- | :--- | :--- |
| `09_chain_of_thought.py` | 思维链推理 | 循环 + 自检 | 自动运行 |
| `10_mcp_tool.py` | MCP 工具集成 | 智能体 + 工具 | 自动运行 |
| `12_agentic_coding/` | 智能体编程 | 完整项目模板 | 自动运行 |

## 运行示例

```bash
# 运行单个示例
python 01_chatbot.py

# 案例 12 是多文件项目，需要进入目录运行
cd 12_agentic_coding
python main.py

# 运行案例 12 的单元测试
cd 12_agentic_coding
python tests/test_nodes.py
```

### 按学习路径运行

```bash
# 零基础入门：ChatBot → 写作工作流 → RAG
python 01_chatbot.py
python 02_writing_workflow.py
python 03_rag.py

# 智能体方向：搜索智能体 → 多智能体 → 智能体技能 → MCP → 智能体编程
python 04_search_agent.py
python 05_multi_agent.py
python 11_agent_skills.py
python 10_mcp_tool.py
cd 12_agentic_coding && python main.py

# 性能方向：Map-Reduce → 并行处理
python 06_map_reduce.py
python 07_parallel_processing.py
```

## 关于模拟实现

所有示例默认使用**模拟的 LLM 和工具函数**，不需要 API 密钥即可运行。这样做的目的是：

1. **降低门槛**：无需注册任何服务，安装 pocketflow 即可体验
2. **聚焦核心**：模拟逻辑让你更清楚每个节点在做什么
3. **易于替换**：每个模拟函数都标注了替换说明，接入真实 API 只需几行修改

### 接入真实 LLM

以案例 12 为例，修改 `12_agentic_coding/utils/call_llm.py`：

```python
# 取消注释 OpenAI 实现部分，注释掉模拟实现
# 设置环境变量：
#   export OPENAI_API_KEY="your-key"
#   export OPENAI_MODEL="gpt-4o-mini"
```

## 兼容性

本教程示例仅依赖 PocketFlow 的核心 API（`Node`、`Flow`、`BatchNode`、`AsyncNode` 等），这些接口自框架发布以来保持稳定。如框架发生重大 API 变更，请参考 [PocketFlow 官方文档](https://the-pocket.github.io/PocketFlow/) 进行调整。

## 项目结构

```
examples/
├── README.md                    # 本文件
├── requirements.txt             # 依赖管理
├── 01_chatbot.py                # 聊天机器人
├── 02_writing_workflow.py       # 写作工作流
├── 03_rag.py                    # RAG 检索增强
├── 04_search_agent.py           # 搜索智能体
├── 05_multi_agent.py            # 多智能体协作
├── 06_map_reduce.py             # Map-Reduce 批处理
├── 07_parallel_processing.py    # 并行处理
├── 08_structured_output.py      # 结构化输出
├── 09_chain_of_thought.py       # 思维链推理
├── 10_mcp_tool.py               # MCP 工具集成
├── 11_agent_skills.py           # 智能体技能路由
└── 12_agentic_coding/           # 智能体编程（完整项目模板）
    ├── main.py                  # 主入口
    ├── nodes.py                 # 节点定义
    ├── flow.py                  # Flow 构建
    ├── utils/                   # 工具函数
    │   ├── __init__.py
    │   ├── call_llm.py          # LLM 调用
    │   └── search_web.py        # 搜索工具
    └── tests/                   # 单元测试
        └── test_nodes.py
```
