"""
案例 07：并行处理 (8x 加速)
对应教程：第 7 节 —— 并行处理

模式：AsyncParallelBatchNode
演示：
- 使用 asyncio.gather() 实现真正的并发
- 对比串行 vs 并行的性能差异
- I/O 密集场景下可获得 N 倍加速

注意：本示例使用模拟异步 API 调用，无需外部服务。
"""

import asyncio
import time
from pocketflow import AsyncNode, AsyncParallelBatchNode, AsyncFlow


# ========== 节点定义 ==========

class SequentialProcess(AsyncNode):
    """串行处理：逐个等待"""

    async def prep_async(self, shared):
        return shared["items"]

    async def exec_async(self, items):
        results = []
        for item in items:
            print(f"  [串行] 处理 {item}...")
            await asyncio.sleep(0.5)  # 模拟 I/O 耗时
            results.append(f"{item} → 完成")
            print(f"  [串行] {item} 完成")
        return results

    async def post_async(self, shared, prep_res, exec_res):
        shared["results"] = exec_res


class ParallelProcess(AsyncParallelBatchNode):
    """并行处理：asyncio.gather() 并发执行"""

    async def prep_async(self, shared):
        items = shared["items"]
        print(f"[并行] 准备并发处理 {len(items)} 个任务")
        return items

    async def exec_async(self, item):
        # 每个 item 并发执行
        print(f"  [并行] 开始处理 {item}...")
        await asyncio.sleep(0.5)  # 模拟 I/O 耗时
        print(f"  [并行] {item} 完成")
        return f"{item} → 完成"

    async def post_async(self, shared, prep_res, exec_res):
        shared["results"] = exec_res
        print(f"[并行] 全部完成，共 {len(exec_res)} 个结果")


# ========== 运行对比 ==========

async def main():
    items = [f"任务_{i + 1}" for i in range(8)]

    # --- 串行执行 ---
    print("=== 串行处理 ===\n")
    seq_node = SequentialProcess()
    seq_flow = AsyncFlow(start=seq_node)
    shared_seq = {"items": items}

    start = time.time()
    await seq_flow.run_async(shared_seq)
    seq_time = time.time() - start
    print(f"\n串行耗时：{seq_time:.2f} 秒\n")

    # --- 并行执行 ---
    print("=" * 40)
    print("\n=== 并行处理 ===\n")
    par_node = ParallelProcess()
    par_flow = AsyncFlow(start=par_node)
    shared_par = {"items": items}

    start = time.time()
    await par_flow.run_async(shared_par)
    par_time = time.time() - start
    print(f"\n并行耗时：{par_time:.2f} 秒")
    print(f"加速比：{seq_time / par_time:.1f}x")


if __name__ == "__main__":
    asyncio.run(main())
