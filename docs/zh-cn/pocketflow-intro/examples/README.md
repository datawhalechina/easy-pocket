# PocketFlow 原理入门 —— 配套示例代码

本文件夹包含 [PocketFlow 原理入门教程](../index.md) 中所有代码示例的**完整可运行版本**。

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

这只会安装 `pocketflow`（零依赖框架），不会引入其他包。

> **备选方案**：PocketFlow 只有 100 行代码，你也可以直接将源码复制到项目中：
> ```bash
> pip install pocketflow
> # 或者从 https://github.com/The-Pocket/PocketFlow 复制 pocketflow/__init__.py
> ```

## 示例列表

| 文件 | 对应章节 | 核心概念 |
| :--- | :--- | :--- |
| `01_hello_pocketflow.py` | 6.2 第一个 Flow | Node + Flow 基础用法 |
| `02_node_lifecycle.py` | 1.1 Node 最小单元 | prep → exec → post 三阶段 |
| `03_flow_chain.py` | 1.2 & 1.3 Flow 图执行 | `>>` 链式连接、图遍历 |
| `04_conditional_flow.py` | 1.3 条件连接 | `- "action" >>` 条件分支 |
| `05_shared_store.py` | 2 Shared 通信 | 节点间通过 shared 传递数据 |
| `06_retry_node.py` | 3.2 重试机制 | max_retries、exec_fallback |
| `07_nested_flow.py` | 3.3 嵌套子流程 | Flow 作为节点参与父 Flow |
| `08_batch_node.py` | 3.4 批量处理 | BatchNode 批量执行 |
| `09_async_parallel.py` | 3.5 异步并发 | AsyncParallelBatchNode |
| `10_loop_pattern.py` | 4 六大设计模式 | 循环/自校正模式 |

## 运行示例

```bash
# 运行单个示例
python 01_hello_pocketflow.py

# 按顺序运行所有示例
python 01_hello_pocketflow.py
python 02_node_lifecycle.py
python 03_flow_chain.py
python 04_conditional_flow.py
python 05_shared_store.py
python 06_retry_node.py
python 07_nested_flow.py
python 08_batch_node.py
python 09_async_parallel.py
python 10_loop_pattern.py
```

## 说明

- 所有示例都是**自包含的**，不需要 API 密钥或外部服务
- LLM 调用使用模拟逻辑代替，便于理解核心概念
- 示例编号与教程章节顺序对应，建议按顺序学习
- 如需接入真实 LLM API，只需替换 `exec()` 中的模拟逻辑即可

## 兼容性

本教程示例仅依赖 PocketFlow 的核心 API（`Node`、`Flow`、`BatchNode`、`AsyncNode` 等），这些接口自框架发布以来保持稳定。如框架发生重大 API 变更，请参考 [PocketFlow 官方文档](https://the-pocket.github.io/PocketFlow/) 进行调整。
