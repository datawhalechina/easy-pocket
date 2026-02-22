<!--
  CaseShowcase.vue
  PocketFlow 应用案例展示组件

  用途：
  展示 PocketFlow 的各种应用场景，通过卡片和流程图
  让读者理解如何用 Node + Flow 构建实际的 LLM 应用

  交互功能：
  - 按难度/类型筛选案例
  - 点击案例查看 Flow 架构图和关键代码
-->
<template>
  <div class="case-showcase">
    <div class="header">
      <span class="icon">🎯</span>
      <span class="title">PocketFlow 应用案例全景</span>
    </div>

    <div class="filter-bar">
      <button
        v-for="cat in categories"
        :key="cat.id"
        :class="['filter-btn', { active: activeCategory === cat.id }]"
        @click="activeCategory = cat.id"
      >
        {{ cat.icon }} {{ cat.label }}
      </button>
    </div>

    <div class="cases-grid">
      <div
        v-for="c in filteredCases"
        :key="c.id"
        :class="['case-card', { expanded: expandedCase === c.id }]"
        @click="toggleCase(c.id)"
      >
        <div class="case-header">
          <div class="case-icon">{{ c.icon }}</div>
          <div class="case-meta">
            <div class="case-name">{{ c.name }}</div>
            <div class="case-tags">
              <span class="tag difficulty" :class="c.difficulty">{{ c.diffLabel }}</span>
              <span class="tag type">{{ c.type }}</span>
            </div>
          </div>
        </div>
        <div class="case-desc">{{ c.desc }}</div>

        <div class="case-detail" v-if="expandedCase === c.id">
          <div class="detail-section">
            <div class="detail-label">Flow 架构</div>
            <div class="flow-diagram">
              <span v-for="(step, i) in c.flow" :key="i" class="flow-step">
                <span class="step-node">{{ step }}</span>
                <span v-if="i < c.flow.length - 1" class="step-arrow">→</span>
              </span>
            </div>
          </div>
          <div class="detail-section">
            <div class="detail-label">核心代码</div>
            <pre class="detail-code"><code>{{ c.code }}</code></pre>
          </div>
          <div class="detail-section">
            <div class="detail-label">关键学习点</div>
            <ul class="detail-points">
              <li v-for="(pt, i) in c.points" :key="i">{{ pt }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const categories = [
  { id: 'all', icon: '📋', label: '全部' },
  { id: 'basic', icon: '🌱', label: '入门' },
  { id: 'agent', icon: '🤖', label: 'Agent' },
  { id: 'data', icon: '📊', label: '数据处理' },
  { id: 'advanced', icon: '🚀', label: '进阶' }
]

const cases = [
  {
    id: 'chat',
    icon: '💬',
    name: '聊天机器人',
    category: 'basic',
    difficulty: 'easy',
    diffLabel: '入门',
    type: '对话',
    anchor: '_1-聊天机器人-chatbot',
    desc: '最基础的 ChatBot —— 维护对话历史，调用 LLM 生成回复，支持多轮对话。',
    flow: ['GetInput', 'CallLLM', 'SendReply'],
    code: `get_input >> call_llm >> send_reply
send_reply - "continue" >> get_input  # 循环对话`,
    points: ['Node 间通过 shared["history"] 传递对话历史', '循环模式：post() 返回 "continue" 实现多轮']
  },
  {
    id: 'workflow',
    icon: '📝',
    name: '写作工作流',
    category: 'basic',
    difficulty: 'easy',
    diffLabel: '入门',
    type: '工作流',
    anchor: '_2-写作工作流-writing-workflow',
    desc: '多步骤写作流程：先列大纲，再分章节撰写，最后统一润色风格。',
    flow: ['Outline', 'WriteDraft', 'Polish'],
    code: `outline >> write_draft >> polish
flow = Flow(start=outline)
flow.run({"topic": "AI 编程入门"})`,
    points: ['链式 Flow 的经典应用', 'shared 逐步累积中间产物', '每个节点专注一个写作阶段']
  },
  {
    id: 'rag',
    icon: '📚',
    name: 'RAG 检索增强生成',
    category: 'basic',
    difficulty: 'easy',
    diffLabel: '入门',
    type: '检索',
    anchor: '_3-rag-检索增强生成',
    desc: '经典 RAG 流程：离线构建向量索引，在线检索相关文档片段并增强 LLM 生成。',
    flow: ['Chunking', 'Embedding', 'Indexing', 'Retrieval', 'Generation'],
    code: `# 离线索引
chunk >> embed >> index
# 在线查询
retrieve >> generate`,
    points: ['BatchNode 批量处理文档切片', '向量相似度搜索 Top-K 文档', 'Prompt 模板拼接 context + question']
  },
  {
    id: 'agent',
    icon: '🕵️',
    name: '搜索 Agent',
    category: 'agent',
    difficulty: 'medium',
    diffLabel: '中级',
    type: 'Agent',
    anchor: '_4-搜索-agent',
    desc: '能够调用搜索工具的研究 Agent —— 理解问题、搜索网络、整合答案。',
    flow: ['Think', 'Search', 'Synthesize'],
    code: `think - "need_more" >> search
think - "enough" >> synthesize
search >> think  # 搜索后回到思考`,
    points: ['条件分支实现 Agent 自主决策', 'Tool-use 模式：exec() 调用外部工具', '循环搜索直到信息充分']
  },
  {
    id: 'multi-agent',
    icon: '👥',
    name: '多 Agent 协作',
    category: 'agent',
    difficulty: 'medium',
    diffLabel: '中级',
    type: 'Agent',
    anchor: '_5-多-agent-协作',
    desc: 'Taboo 猜词游戏 —— 两个 AsyncNode Agent 通过消息队列异步通信，asyncio.gather 并发运行。',
    flow: ['HinterAgent', 'GuesserAgent'],
    code: `hinter - "continue" >> hinter  # 自循环
guesser - "continue" >> guesser
await asyncio.gather(hinter_flow.run_async(shared),
                     guesser_flow.run_async(shared))`,
    points: ['AsyncNode 异步三阶段执行', 'asyncio.Queue 实现 Agent 间消息传递', 'asyncio.gather 并发运行多个 Agent']
  },
  {
    id: 'map-reduce',
    icon: '🗂️',
    name: 'Map-Reduce 批处理',
    category: 'data',
    difficulty: 'easy',
    diffLabel: '入门',
    type: '数据处理',
    anchor: '_6-map-reduce-批处理',
    desc: '批量评估简历 —— 并行处理每份简历，最后汇总排名。',
    flow: ['LoadResumes', 'EvalBatch', 'Aggregate'],
    code: `load >> eval_batch >> aggregate
# eval_batch 使用 BatchNode
# 自动对每份简历独立执行 exec()`,
    points: ['BatchNode 自动处理列表', 'prep() 返回简历列表', 'post() 汇总所有评分结果']
  },
  {
    id: 'parallel',
    icon: '⚡',
    name: '并行图片处理',
    category: 'data',
    difficulty: 'medium',
    diffLabel: '中级',
    type: '数据处理',
    anchor: '_7-并行处理-8x-加速',
    desc: '使用 AsyncParallelBatchNode 并行处理多张图片，实现 8x 加速。',
    flow: ['LoadImages', 'ParallelFilter', 'SaveResults'],
    code: `load >> parallel_filter >> save
# parallel_filter 使用 AsyncParallelBatchNode
# asyncio.gather() 并发处理`,
    points: ['AsyncParallelBatchNode 实现真并发', 'I/O 密集任务获得数倍加速', '与同步版本代码结构完全一致']
  },
  {
    id: 'structured-output',
    icon: '📋',
    name: '结构化输出',
    category: 'advanced',
    difficulty: 'medium',
    diffLabel: '中级',
    type: '可靠性',
    anchor: '_8-结构化输出-structured-output',
    desc: '让 LLM 输出严格 JSON 格式 —— 生成、解析校验、格式不对则自动重新生成。',
    flow: ['Generate', 'Validate', 'Check'],
    code: `generate >> validate >> check
check - "retry" >> generate  # 格式不对，重来
check - "done" >> output`,
    points: ['双层重试：节点内解析重试 + Flow 层生成重试', 'exec_fallback 返回 None 触发重新生成', '正则提取 + JSON 解析 + 字段校验']
  },
  {
    id: 'thinking',
    icon: '🧠',
    name: '思维链推理',
    category: 'advanced',
    difficulty: 'hard',
    diffLabel: '进阶',
    type: '推理',
    anchor: '_9-思维链推理-chain-of-thought',
    desc: '实现 Chain-of-Thought 推理 —— 分步思考，逐步求解复杂问题。',
    flow: ['Decompose', 'StepReason', 'Verify', 'Conclude'],
    code: `decompose >> step_reason >> verify
verify - "error" >> step_reason  # 发现错误重推
verify - "ok" >> conclude`,
    points: ['循环推理直到验证通过', 'exec() 中显式要求 LLM 输出思考过程', '自检机制提高推理准确性']
  },
  {
    id: 'mcp',
    icon: '🔌',
    name: 'MCP 工具集成',
    category: 'advanced',
    difficulty: 'hard',
    diffLabel: '进阶',
    type: '集成',
    anchor: '_10-mcp-工具集成',
    desc: '通过 Model Context Protocol 集成外部工具，构建具备丰富工具使用能力的 Agent。',
    flow: ['Plan', 'SelectTool', 'Execute', 'Reflect'],
    code: `plan >> select_tool >> execute >> reflect
reflect - "done" >> output
reflect - "continue" >> plan`,
    points: ['MCP 协议标准化工具调用', 'Agent 自主选择和使用工具', '反思循环优化执行结果']
  },
  {
    id: 'agentic-coding',
    icon: '🤝',
    name: '智能体编程',
    category: 'advanced',
    difficulty: 'hard',
    diffLabel: '进阶',
    type: '方法论',
    anchor: '_11-智能体编程-agentic-coding',
    desc: '人类设计 + AI 实现的高效协作范式 —— 8 步流程从需求到可靠系统的完整工程实践。',
    flow: ['Requirements', 'Flow设计', 'Utilities', 'Data', 'Node', 'Implementation', 'Optimization', 'Reliability'],
    code: `# 设计文档优先
docs/design.md  # 先写设计
utils/  # 实现工具
nodes.py + flow.py + main.py  # Agent 实现`,
    points: ['人类负责系统设计，AI 负责实现', '设计文档是数据契约', '小步迭代 + Fail Fast + 可靠性补齐']
  }
]

const activeCategory = ref('all')
const expandedCase = ref(null)

const filteredCases = computed(() => {
  if (activeCategory.value === 'all') return cases
  return cases.filter((c) => c.category === activeCategory.value)
})

const toggleCase = (id) => {
  if (expandedCase.value === id) {
    // 已展开，跳转到对应章节
    const c = cases.find((item) => item.id === id)
    if (c?.anchor) {
      const el = document.getElementById(c.anchor)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' })
        history.replaceState(null, '', '#' + c.anchor)
      }
    }
  } else {
    expandedCase.value = id
  }
}
</script>

<style scoped>
.case-showcase {
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

.icon { font-size: 1.5rem; }
.title { font-size: 1.15rem; font-weight: 700; color: var(--vp-c-text-1); }

.filter-bar {
  display: flex;
  gap: 0.4rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.35rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  cursor: pointer;
  font-size: 0.83rem;
  color: var(--vp-c-text-2);
  transition: all 0.2s;
}

.filter-btn:hover { border-color: var(--vp-c-brand); }
.filter-btn.active { background: var(--vp-c-brand); color: #fff; border-color: var(--vp-c-brand); }

.cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.75rem;
}

.case-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  padding: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.case-card:hover { border-color: var(--vp-c-brand); }
.case-card.expanded { grid-column: 1 / -1; border-color: var(--vp-c-brand); }

.case-header {
  display: flex;
  gap: 0.65rem;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.case-icon { font-size: 1.8rem; flex-shrink: 0; }
.case-name { font-weight: 700; font-size: 0.95rem; color: var(--vp-c-text-1); }

.case-tags {
  display: flex;
  gap: 0.3rem;
  margin-top: 0.2rem;
}

.tag {
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
}

.tag.difficulty.easy { background: #e8f5e9; color: #2e7d32; }
.tag.difficulty.medium { background: #fff3e0; color: #e65100; }
.tag.difficulty.hard { background: #fce4ec; color: #c62828; }
.tag.type { background: var(--vp-c-bg-soft); color: var(--vp-c-text-3); }

.case-desc {
  font-size: 0.83rem;
  color: var(--vp-c-text-3);
  line-height: 1.5;
}

.case-detail {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--vp-c-divider);
}

.detail-section {
  margin-bottom: 0.75rem;
}

.detail-label {
  font-weight: 700;
  font-size: 0.83rem;
  color: var(--vp-c-text-1);
  margin-bottom: 0.35rem;
}

.flow-diagram {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
  padding: 0.5rem;
  background: var(--vp-c-bg-soft);
  border-radius: 6px;
}

.step-node {
  background: var(--vp-c-brand);
  color: #fff;
  padding: 0.25rem 0.6rem;
  border-radius: 5px;
  font-size: 0.78rem;
  font-weight: 500;
}

.step-arrow { color: var(--vp-c-text-3); font-size: 0.9rem; }

.detail-code {
  background: var(--vp-c-bg-alt);
  border-radius: 6px;
  padding: 0.65rem;
  margin: 0;
  font-size: 0.78rem;
  line-height: 1.5;
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-text-2);
  overflow-x: auto;
}

.detail-points {
  margin: 0;
  padding-left: 1.25rem;
  font-size: 0.82rem;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.detail-points li { margin-bottom: 0.15rem; }

@media (max-width: 640px) {
  .cases-grid { grid-template-columns: 1fr; }
}
</style>
