"""
示例 09：AsyncNode 与 AsyncParallelBatchNode 异步并发
对应教程：第 3.5 节 —— AsyncNode 异步并发

演示：
- AsyncNode 的 async/await 三阶段执行
- AsyncParallelBatchNode 使用 asyncio.gather() 实现真正的并发
- 对比串行 vs 并行的效率差异
"""

import asyncio
import time
from pocketflow import AsyncNode, AsyncParallelBatchNode, AsyncFlow


class FetchUrlNode(AsyncParallelBatchNode):
    """并行获取多个 URL 的内容（模拟）"""

    async def prep_async(self, shared):
        urls = shared.get("urls", [])
        print(f"[AsyncParallel] 准备并行获取 {len(urls)} 个 URL")
        return urls

    async def exec_async(self, url):
        # 模拟异步 HTTP 请求（每个耗时 1 秒）
        print(f"  开始获取：{url}")
        await asyncio.sleep(1)  # 模拟网络延迟
        result = f"内容来自 {url}"
        print(f"  完成获取：{url}")
        return result

    async def post_async(self, shared, prep_res, exec_res):
        shared["results"] = exec_res
        print(f"\n[AsyncParallel] 全部完成，共 {len(exec_res)} 个结果")


class SequentialFetchNode(AsyncNode):
    """串行获取 URL（用于对比）"""

    async def prep_async(self, shared):
        return shared.get("urls", [])

    async def exec_async(self, urls):
        results = []
        for url in urls:
            print(f"  开始获取：{url}")
            await asyncio.sleep(1)
            results.append(f"内容来自 {url}")
            print(f"  完成获取：{url}")
        return results

    async def post_async(self, shared, prep_res, exec_res):
        shared["results"] = exec_res


async def main():
    urls = [
        "https://api.example.com/data1",
        "https://api.example.com/data2",
        "https://api.example.com/data3",
        "https://api.example.com/data4",
    ]

    # --- 串行执行 ---
    print("=== 串行获取（逐个等待）===\n")
    sequential_node = SequentialFetchNode()
    sequential_flow = AsyncFlow(start=sequential_node)
    shared_seq = {"urls": urls}

    start = time.time()
    await sequential_flow.run_async(shared_seq)
    seq_time = time.time() - start
    print(f"\n串行耗时：{seq_time:.2f} 秒\n")

    # --- 并行执行 ---
    print("=" * 40)
    print("=== 并行获取（asyncio.gather）===\n")
    parallel_node = FetchUrlNode()
    parallel_flow = AsyncFlow(start=parallel_node)
    shared_par = {"urls": urls}

    start = time.time()
    await parallel_flow.run_async(shared_par)
    par_time = time.time() - start
    print(f"\n并行耗时：{par_time:.2f} 秒")
    print(f"加速比：{seq_time / par_time:.1f}x")


if __name__ == "__main__":
    asyncio.run(main())
