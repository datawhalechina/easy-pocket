<!--
  CoreCodeDemo.vue
  PocketFlow 核心源码交互式解读组件

  用途：
  分层展示 PocketFlow 100 行核心源码的 5 个关键类，
  让读者逐层点击理解 BaseNode → Node → Flow → BatchNode → AsyncNode

  交互功能：
  - 点击不同的类标签切换代码高亮区域
  - 每个类附带功能说明和关系图
  - 代码行内高亮关键逻辑
-->
<template>
  <div class="core-code-demo">
    <div class="header">
      <span class="icon">🔬</span>
      <span class="title">PocketFlow 核心源码解剖</span>
    </div>

    <div class="class-tabs">
      <button
        v-for="cls in classes"
        :key="cls.id"
        :class="['tab-btn', { active: activeClass === cls.id }]"
        @click="activeClass = cls.id"
      >
        <span class="tab-icon">{{ cls.icon }}</span>
        <span>{{ cls.name }}</span>
      </button>
    </div>

    <div class="content-area">
      <div class="code-panel">
        <div class="code-header">
          <span class="file-name">pocketflow/__init__.py</span>
          <span class="line-count">{{ activeClassData.lineRange }}</span>
        </div>
        <pre class="code-block"><code v-html="activeClassData.code"></code></pre>
      </div>

      <div class="explain-panel">
        <div class="explain-title">{{ activeClassData.title }}</div>
        <div class="explain-role">
          <span class="role-label">角色</span>
          <span class="role-text">{{ activeClassData.role }}</span>
        </div>
        <div class="explain-points">
          <div v-for="(point, i) in activeClassData.points" :key="i" class="point">
            <span class="point-num">{{ i + 1 }}</span>
            <span class="point-text">{{ point }}</span>
          </div>
        </div>
        <div class="explain-analogy" v-if="activeClassData.analogy">
          <span class="analogy-icon">🎯</span>
          <span>{{ activeClassData.analogy }}</span>
        </div>
      </div>
    </div>

    <div class="hierarchy">
      <div class="hierarchy-title">继承关系</div>
      <pre class="hierarchy-tree"><span :class="{ highlight: activeClass === 'basenode' }">BaseNode</span>
├─ <span :class="{ highlight: activeClass === 'node' }">Node</span>
│  ├─ <span :class="{ highlight: activeClass === 'batch' }">BatchNode</span>
│  └─ <span :class="{ highlight: activeClass === 'async' }">AsyncNode</span>
└─ <span :class="{ highlight: activeClass === 'flow' }">Flow</span>
   └─ BatchFlow / AsyncFlow</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeClass = ref('basenode')

const classes = [
  { id: 'basenode', icon: '🧱', name: 'BaseNode' },
  { id: 'node', icon: '⚙️', name: 'Node' },
  { id: 'flow', icon: '🔄', name: 'Flow' },
  { id: 'batch', icon: '📦', name: 'BatchNode' },
  { id: 'async', icon: '⚡', name: 'AsyncNode' }
]

const classDetails = {
  basenode: {
    title: 'BaseNode — 万物之基',
    lineRange: 'Lines 3-15',
    role: '定义节点的基础结构：参数管理、后继连接、三阶段执行',
    code: `<span class="kw">class</span> <span class="cls">BaseNode</span>:
    <span class="kw">def</span> <span class="fn">__init__</span>(self):
        self.<span class="hl">params</span>, self.<span class="hl">successors</span> = {}, {}

    <span class="kw">def</span> <span class="fn">next</span>(self, node, action=<span class="str">"default"</span>):
        self.successors[action] = node
        <span class="kw">return</span> node

    <span class="cm"># 三阶段执行模型</span>
    <span class="kw">def</span> <span class="fn">prep</span>(self, shared): <span class="kw">pass</span>
    <span class="kw">def</span> <span class="fn">exec</span>(self, prep_res): <span class="kw">pass</span>
    <span class="kw">def</span> <span class="fn">post</span>(self, shared, prep_res, exec_res): <span class="kw">pass</span>

    <span class="kw">def</span> <span class="fn">_run</span>(self, shared):
        p = self.prep(shared)
        e = self._exec(p)
        <span class="kw">return</span> self.post(shared, p, e)

    <span class="cm"># 操作符重载：node1 >> node2</span>
    <span class="kw">def</span> <span class="fn">__rshift__</span>(self, other):
        <span class="kw">return</span> self.next(other)

    <span class="cm"># 条件转移：node1 - "action" >> node2</span>
    <span class="kw">def</span> <span class="fn">__sub__</span>(self, action):
        <span class="kw">return</span> _ConditionalTransition(self, action)`,
    points: [
      'params 字典存储节点参数，successors 字典存储后继节点映射',
      'next() 方法将两个节点通过 action 字符串连接，构成有向图的边',
      'prep → exec → post 三阶段是核心执行模型：准备数据、执行逻辑、后处理',
      '>> 操作符让你可以写 nodeA >> nodeB 来连接节点',
      '- 操作符支持条件分支：nodeA - "yes" >> nodeB'
    ],
    analogy: '类比：BaseNode 就像乐高积木的基础底板，定义了所有积木块的通用接口。'
  },
  node: {
    title: 'Node — 可重试的执行单元',
    lineRange: 'Lines 17-24',
    role: '继承 BaseNode，增加重试机制和等待间隔',
    code: `<span class="kw">class</span> <span class="cls">Node</span>(<span class="cls">BaseNode</span>):
    <span class="kw">def</span> <span class="fn">__init__</span>(self, <span class="hl">max_retries</span>=1, <span class="hl">wait</span>=0):
        <span class="kw">super</span>().__init__()
        self.max_retries = max_retries
        self.wait = wait

    <span class="kw">def</span> <span class="fn">exec_fallback</span>(self, prep_res, exc):
        <span class="kw">raise</span> exc

    <span class="kw">def</span> <span class="fn">_exec</span>(self, prep_res):
        <span class="kw">for</span> self.cur_retry <span class="kw">in</span> range(self.max_retries):
            <span class="kw">try</span>:
                <span class="kw">return</span> self.exec(prep_res)
            <span class="kw">except</span> Exception <span class="kw">as</span> e:
                <span class="kw">if</span> self.cur_retry == self.max_retries - 1:
                    <span class="kw">return</span> self.exec_fallback(prep_res, e)
                <span class="kw">if</span> self.wait > 0:
                    time.sleep(self.wait)`,
    points: [
      'max_retries 控制最大重试次数，默认 1（不重试）',
      'wait 参数指定重试间隔秒数，用于应对 API 限流等场景',
      '_exec() 覆写了父类方法，在循环中尝试执行 exec()',
      '最后一次失败会调用 exec_fallback()，默认抛出异常',
      '你可以覆写 exec_fallback() 来实现优雅降级'
    ],
    analogy: '类比：Node 就像一个有耐心的快递员 —— 送不到就再试一次，实在不行就走备选方案。'
  },
  flow: {
    title: 'Flow — 图执行引擎',
    lineRange: 'Lines 28-38',
    role: '核心编排器：从 start_node 开始，沿有向图逐节点执行',
    code: `<span class="kw">class</span> <span class="cls">Flow</span>(<span class="cls">BaseNode</span>):
    <span class="kw">def</span> <span class="fn">__init__</span>(self, start=<span class="kw">None</span>):
        <span class="kw">super</span>().__init__()
        self.<span class="hl">start_node</span> = start

    <span class="kw">def</span> <span class="fn">get_next_node</span>(self, curr, action):
        nxt = curr.successors.get(action <span class="kw">or</span> <span class="str">"default"</span>)
        <span class="kw">return</span> nxt

    <span class="kw">def</span> <span class="fn">_orch</span>(self, shared, params=<span class="kw">None</span>):
        curr = copy.copy(self.start_node)
        p = params <span class="kw">or</span> {**self.params}
        last_action = <span class="kw">None</span>
        <span class="cm"># 核心循环：执行当前节点 → 获取下一个</span>
        <span class="kw">while</span> curr:
            curr.set_params(p)
            last_action = curr._run(shared)
            curr = copy.copy(
                self.get_next_node(curr, last_action)
            )
        <span class="kw">return</span> last_action

    <span class="kw">def</span> <span class="fn">_run</span>(self, shared):
        p = self.prep(shared)
        o = self._orch(shared)
        <span class="kw">return</span> self.post(shared, p, o)`,
    points: [
      'Flow 本身也继承自 BaseNode，因此 Flow 可以嵌套在其他 Flow 中',
      '_orch() 是核心编排方法：while 循环遍历图中的节点',
      '每个节点执行后返回 action 字符串，决定走向哪个后继节点',
      'copy.copy() 确保每次执行使用节点的浅拷贝，避免状态污染',
      'shared 字典在所有节点间共享，是节点间通信的唯一渠道'
    ],
    analogy: '类比：Flow 就像一个项目经理 —— 按照流程图依次安排每个人的工作，根据结果决定下一步。'
  },
  batch: {
    title: 'BatchNode — 批量处理器',
    lineRange: 'Lines 26-27',
    role: '对列表中的每个元素独立执行 Node 的逻辑',
    code: `<span class="kw">class</span> <span class="cls">BatchNode</span>(<span class="cls">Node</span>):
    <span class="kw">def</span> <span class="fn">_exec</span>(self, items):
        <span class="kw">return</span> [
            <span class="kw">super</span>(BatchNode, self)._exec(i)
            <span class="kw">for</span> i <span class="kw">in</span> (items <span class="kw">or</span> [])
        ]

<span class="cm"># 使用示例：</span>
<span class="cm"># prep() 返回一个列表 [item1, item2, ...]</span>
<span class="cm"># exec() 对每个 item 执行一次</span>
<span class="cm"># post() 收到所有结果的列表</span>`,
    points: [
      '仅覆写了 _exec() 方法，将列表中每个元素逐一传递给父类 Node 的 _exec()',
      'prep() 需要返回一个可迭代对象（列表），每个元素会被独立处理',
      '继承了 Node 的重试机制 —— 每个元素的处理都有独立的重试',
      '结果以列表形式返回，保持与输入的一一对应关系'
    ],
    analogy: '类比：BatchNode 就像流水线上的质检员 —— 同样的检查逻辑，对每个产品逐一执行。'
  },
  async: {
    title: 'AsyncNode — 异步执行单元',
    lineRange: 'Lines 40-55',
    role: '提供 async/await 版本的三阶段执行，支持并发',
    code: `<span class="kw">class</span> <span class="cls">AsyncNode</span>(<span class="cls">Node</span>):
    <span class="kw">async def</span> <span class="fn">prep_async</span>(self, shared): <span class="kw">pass</span>
    <span class="kw">async def</span> <span class="fn">exec_async</span>(self, prep_res): <span class="kw">pass</span>
    <span class="kw">async def</span> <span class="fn">post_async</span>(self, shared, p, e): <span class="kw">pass</span>

    <span class="kw">async def</span> <span class="fn">_exec</span>(self, prep_res):
        <span class="kw">for</span> self.cur_retry <span class="kw">in</span> range(self.max_retries):
            <span class="kw">try</span>:
                <span class="kw">return await</span> self.exec_async(prep_res)
            <span class="kw">except</span> Exception <span class="kw">as</span> e:
                <span class="kw">if</span> self.cur_retry == self.max_retries - 1:
                    <span class="kw">return await</span> self.exec_fallback_async(...)
                <span class="kw">if</span> self.wait > 0:
                    <span class="kw">await</span> asyncio.sleep(self.wait)

<span class="cm"># AsyncParallelBatchNode：并发批处理</span>
<span class="kw">class</span> <span class="cls">AsyncParallelBatchNode</span>(<span class="cls">AsyncNode</span>):
    <span class="kw">async def</span> <span class="fn">_exec</span>(self, items):
        <span class="kw">return await</span> asyncio.gather(
            *(super()._exec(i) <span class="kw">for</span> i <span class="kw">in</span> items)
        )`,
    points: [
      '提供 prep_async / exec_async / post_async 三个异步方法',
      '重试间隔使用 asyncio.sleep() 而非 time.sleep()，不阻塞事件循环',
      'AsyncParallelBatchNode 使用 asyncio.gather() 实现真正的并发执行',
      '并发批处理可以获得数倍的性能提升（如 8x speedup）',
      '适合调用多个 API、处理多个文件等 I/O 密集场景'
    ],
    analogy: '类比：AsyncNode 像分配给多个厨师同时做菜，而不是一个厨师顺序做完。'
  }
}

const activeClassData = computed(() => classDetails[activeClass.value])
</script>

<style scoped>
.core-code-demo {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.icon {
  font-size: 1.5rem;
}

.title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.class-tabs {
  display: flex;
  gap: 0.4rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  transition: all 0.2s;
}

.tab-btn:hover {
  border-color: var(--vp-c-brand);
}

.tab-btn.active {
  background: var(--vp-c-brand);
  color: #fff;
  border-color: var(--vp-c-brand);
}

.tab-icon {
  font-size: 1rem;
}

.content-area {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.code-panel {
  background: var(--vp-c-bg-alt);
  border-radius: 8px;
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  background: var(--vp-c-bg);
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 0.78rem;
  color: var(--vp-c-text-3);
}

.code-block {
  padding: 0.75rem;
  margin: 0;
  font-size: 0.78rem;
  line-height: 1.6;
  overflow-x: auto;
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-text-2);
}

.code-block :deep(.kw) {
  color: #c678dd;
}

.code-block :deep(.cls) {
  color: #e5c07b;
  font-weight: 600;
}

.code-block :deep(.fn) {
  color: #61afef;
}

.code-block :deep(.str) {
  color: #98c379;
}

.code-block :deep(.cm) {
  color: #7f848e;
  font-style: italic;
}

.code-block :deep(.hl) {
  background: rgba(66, 133, 244, 0.15);
  padding: 0 2px;
  border-radius: 2px;
}

.explain-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.explain-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.explain-role {
  display: flex;
  gap: 0.5rem;
  align-items: baseline;
}

.role-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--vp-c-brand);
  background: rgba(66, 133, 244, 0.1);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.role-text {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

.explain-points {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.point {
  display: flex;
  gap: 0.5rem;
  align-items: baseline;
  font-size: 0.83rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
}

.point-num {
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--vp-c-brand);
  color: #fff;
  border-radius: 50%;
  font-size: 0.7rem;
  font-weight: 600;
  flex-shrink: 0;
}

.explain-analogy {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  font-size: 0.83rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
}

.analogy-icon {
  margin-right: 0.25rem;
}

.hierarchy {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 0.75rem 1rem;
}

.hierarchy-title {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.5rem;
}

.hierarchy-tree {
  font-family: var(--vp-font-family-mono);
  font-size: 0.82rem;
  line-height: 1.7;
  color: var(--vp-c-text-3);
  margin: 0;
  padding: 0;
  white-space: pre;
}

.hierarchy-tree .highlight {
  color: var(--vp-c-brand);
  font-weight: 700;
}

@media (max-width: 768px) {
  .content-area {
    grid-template-columns: 1fr;
  }
}
</style>
