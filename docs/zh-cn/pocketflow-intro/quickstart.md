---
title: '快速上手'
description: '环境搭建、安装 PocketFlow 并运行你的第一个 Flow。'
---

# 1. 快速上手

先跑起来，再理解原理。如果你更喜欢看视频，可以先看 [官方视频教程](https://youtu.be/0Zr3NwcvpA0)，配合 [官方文档](https://the-pocket.github.io/PocketFlow/) 一起学习。

### 1.1 环境配置

#### Python 版本

PocketFlow 需要 **Python 3.9+**（推荐 3.10 或更高版本）：

```bash
python --version
```

#### 创建虚拟环境（推荐）

::: code-group

```bash [Windows]
python -m venv .venv
.venv\Scripts\activate
```

```bash [macOS / Linux]
python -m venv .venv
source .venv/bin/activate
```

:::

### 1.2 安装 PocketFlow

::: code-group

```bash [pip]
pip install pocketflow
```

```bash [指定版本]
# 如需锁定版本（教程编写时为 0.0.3）
pip install pocketflow==0.0.3
```

```bash [复制源码]
# PocketFlow 只有 100 行，也可以直接复制到项目中
# https://github.com/The-Pocket/PocketFlow/blob/main/pocketflow/__init__.py
```

:::

::: tip 零依赖
PocketFlow 没有任何第三方依赖，安装后即可直接使用，不会影响你现有的项目环境。
:::

### 1.3 第一个 Flow：Hello PocketFlow

```python
from pocketflow import Node, Flow

class GreetNode(Node):
    def prep(self, shared):
        return shared.get("name", "World")

    def exec(self, name):
        return f"Hello, {name}! Welcome to PocketFlow."

    def post(self, shared, prep_res, exec_res):
        shared["greeting"] = exec_res
        print(exec_res)

# 构建并运行
greet = GreetNode()
flow = Flow(start=greet)
flow.run({"name": "小明"})
# 输出：Hello, 小明! Welcome to PocketFlow.
```

### 1.4 配套示例代码

本教程的所有代码示例都已整理为**完整可运行的 Python 脚本**，存放在 [`examples/`](https://github.com/zhimin-z/easy-pocket/tree/main/docs/zh-cn/pocketflow-intro/examples) 文件夹中：

| 文件 | 对应章节 | 核心概念 |
| :--- | :--- | :--- |
| `01_hello_pocketflow.py` | 1.3 第一个 Flow | Node + Flow 基础用法 |
| `02_node_lifecycle.py` | [2.1 Node 最小单元](./core-abstractions#_2-1-node-——-执行的最小单元) | prep → exec → post 三阶段 |
| `03_flow_chain.py` | [2.2 & 2.3 图执行](./core-abstractions#_2-2-flow-——-图编排引擎) | `>>` 链式连接 |
| `04_conditional_flow.py` | [2.3 条件连接](./core-abstractions#_2-3-连接节点的两种方式) | `- "action" >>` 条件分支 |
| `05_shared_store.py` | [3 通信机制](./communication-and-patterns#_3-通信机制-shared-store-与-params) | 节点间数据传递 |
| `06_retry_node.py` | [5.2 重试机制](./source-code#_5-2-node-——-可重试的执行单元) | max_retries、exec_fallback |
| `07_nested_flow.py` | [5.3 嵌套子流程](./source-code#_5-3-flow-——-图执行引擎) | Flow 作为节点 |
| `08_batch_node.py` | [5.4 批量处理](./source-code#_5-4-batchnode-——-批量处理) | BatchNode |
| `09_async_parallel.py` | [5.6 异步家族](./source-code#_5-6-asyncnode-与异步家族) | AsyncParallelBatchNode |
| `10_loop_pattern.py` | [4 设计模式](./communication-and-patterns#_4-六大设计模式) | 循环/自校正 |

::: info 关于示例代码
- 所有示例**自包含**，不需要 API 密钥或外部服务
- LLM 调用使用模拟逻辑代替，便于理解核心机制
- 如需接入真实 LLM，只需替换 `exec()` 中的模拟逻辑即可
:::
