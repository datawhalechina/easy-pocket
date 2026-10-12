"""离线验证示例和教程中的多智能体退出协议，使用真实 PocketFlow。"""

import asyncio
import contextlib
import importlib.util
import io
from pathlib import Path
import types
import unittest
from unittest.mock import AsyncMock, patch
import warnings

from pocketflow import AsyncFlow


EXAMPLES = Path(__file__).resolve().parents[1]


def load_agents(source):
    if source == "example":
        spec = importlib.util.spec_from_file_location(
            "multi_agent_example", EXAMPLES / "05_multi_agent.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, module.HinterAgent, module.GuesserAgent

    # 执行教程的原代码块，仅移除启动入口；不复制节点实现。
    document = (EXAMPLES.parent / "agents.md").read_text(encoding="utf-8")
    section = document.split("### 5.3 核心代码", 1)[1]
    code = section.split("```python", 1)[1].split("```", 1)[0]
    code = code.rsplit("asyncio.run(main())", 1)[0]
    module = types.ModuleType("multi_agent_tutorial")
    exec(compile(code, "agents.md", "exec"), module.__dict__)
    return module, module.Hinter智能体, module.Guesser智能体


def mock_models(module, source, guesses):
    hinter = AsyncMock(return_value="提示")
    guesser = AsyncMock(side_effect=guesses)
    if source == "example":
        replacements = {"mock_hinter_llm": hinter, "mock_guesser_llm": guesser}
    else:
        async def call_llm(prompt):
            if prompt.startswith("根据以下描述猜一个词"):
                return await guesser(prompt)
            return await hinter(prompt)
        replacements = {"async_call_llm": call_llm}
    return patch.dict(module.__dict__, replacements), hinter, guesser


class MultiAgentTerminationTests(unittest.IsolatedAsyncioTestCase):
    async def run_game(self, source, guesses, error=None):
        module, Hinter, Guesser = load_agents(source)
        models, hinter_llm, guesser_llm = mock_models(module, source, guesses)
        hinter, guesser = Hinter(), Guesser()
        hinter - "continue" >> hinter
        guesser - "continue" >> guesser
        shared = {
            "word": "大熊猫", "taboo_words": [],
            "hinter_queue": asyncio.Queue(), "guesser_queue": asyncio.Queue(),
        }
        shared["hinter_queue"].put_nowait("start")
        with models, contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
            # 没有 end 后继节点是教程约定的正常结束方式。
            warnings.filterwarnings("ignore", message="Flow ends: 'end' not found")
            tasks = [asyncio.create_task(AsyncFlow(start=node).run_async(shared))
                     for node in (hinter, guesser)]
            try:
                if error is not None:
                    with self.assertRaises(type(error)) as raised:
                        await asyncio.wait_for(asyncio.gather(*tasks), timeout=1)
                    self.assertIs(raised.exception, error)
                    self.assertFalse(shared.get("game_over", False))
                else:
                    await asyncio.wait_for(asyncio.gather(*tasks), timeout=1)
                    self.assertTrue(all(task.done() and not task.cancelled() for task in tasks))
                    self.assertTrue(shared["game_over"])
                    self.assertTrue(shared["hinter_queue"].empty())
                    self.assertTrue(shared["guesser_queue"].empty())
            finally:
                # 仅测试清理：旧实现超时或模型异常时取消仍等待消息的伙伴。
                for task in tasks:
                    if not task.done():
                        task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
        self.assertEqual(hinter_llm.await_count, len(guesses))
        self.assertEqual(guesser_llm.await_count, len(guesses))
        return shared

    async def test_first_guess_wins(self):
        for source in ("example", "tutorial"):
            with self.subTest(source=source):
                await self.run_game(source, ["大熊猫"])

    async def test_multiple_rounds_then_win(self):
        for source in ("example", "tutorial"):
            with self.subTest(source=source):
                await self.run_game(source, ["北极熊", "考拉", "大熊猫"])

    async def test_last_allowed_guess_wins(self):
        for source in ("example", "tutorial"):
            with self.subTest(source=source):
                await self.run_game(source, ["考拉"] * 4 + ["大熊猫"])

    async def test_round_limit_ends_both_flows(self):
        for source in ("example", "tutorial"):
            with self.subTest(source=source):
                shared = await self.run_game(source, ["考拉"] * 5)
                self.assertEqual(shared["round"], 5)

    async def test_model_error_is_not_normal_completion(self):
        for source in ("example", "tutorial"):
            with self.subTest(source=source):
                error = RuntimeError("model unavailable")
                await self.run_game(source, [error], error=error)

    async def test_main_reports_five_rounds_when_exhausted(self):
        module, _, _ = load_agents("example")
        models, hinter_llm, guesser_llm = mock_models(module, "example", ["考拉"] * 5)
        output = io.StringIO()
        with models, contextlib.redirect_stdout(output), warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Flow ends: 'end' not found")
            await asyncio.wait_for(module.main(), timeout=1)
        self.assertIn("[游戏结束] 共 5 轮，结果：未猜出", output.getvalue())
        self.assertEqual(hinter_llm.await_count, 5)
        self.assertEqual(guesser_llm.await_count, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
